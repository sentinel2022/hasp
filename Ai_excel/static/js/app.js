$(function(){
  function refreshFiles(){
    $.get('/files', function(data){
      const sel = $('#fileSelect');
      const cur = sel.val();
      sel.empty();
      sel.append('<option value="">请选择已上传的文件</option>');
      data.files.forEach(f => sel.append(`<option value="${f}">${f}</option>`));
      if(data.files.includes(cur)) sel.val(cur);
    });
  }

  $('#refreshFiles').on('click', refreshFiles);
  refreshFiles();

  $('#uploadForm').on('submit', function(e){
    e.preventDefault();
    const file = $('#fileInput')[0].files[0];
    if(!file){ alert('请选择文件后上传'); return; }
    const fd = new FormData(); fd.append('file', file);
    fetch('/upload', {method:'POST', body: fd}).then(r=>r.json()).then(res=>{
      alert('上传成功: '+res.filename);
      refreshFiles();
    }).catch(e=>{ alert('上传失败'); });
  });

  function doSearch(params, onResult){
    showLoading('正在搜索，请稍候…');
    const fd = new FormData();
    fd.append('filename', params.filename);
    fd.append('keyword', params.keyword || '');
    if(params.sheet) fd.append('sheet', params.sheet);
    if(params.page) fd.append('page', params.page);
    if(params.page_size) fd.append('page_size', params.page_size);
    fetch('/search', {method:'POST', body: fd}).then(r=>r.json()).then(res=>{
      const result = res.result || [];
      onResult(result);
    }).catch(e=>{ alert('查询失败'); }).finally(()=>{ hideLoading(); });
  }

  $('#searchBtn').on('click', function(){
    const filename = $('#fileSelect').val();
    const keyword = $('#keyword').val() || '';
    const page_size = parseInt($('#pageSize').val()||20);
    if(!filename){ alert('请选择文件'); return; }
    doSearch({filename: filename, keyword: keyword, page:1, page_size:page_size}, function(result){ renderResults(result, filename, keyword); });
  });

  function renderResults(sheets, filename){
    const container = $('#results'); container.empty();
    if(sheets.length===0){ container.append('<div class="alert alert-info">未找到匹配结果</div>'); return; }
    sheets.forEach(s => {
      const card = $(`<div class="card mb-3"><div class="card-body"></div></div>`);
      const body = card.find('.card-body');
      body.append(`<h5>${s.sheet}</h5>`);
      body.append(`<div class="mb-2"><button class="btn btn-sm btn-outline-primary add-row">新增记录</button></div>`);
      const table = $('<table class="table table-sm table-bordered table-striped table-hover align-middle"></table>');
      const thead = $('<thead class="table-light"></thead>');
      const trh = $('<tr></tr>');
      s.header.forEach(h => trh.append(`<th>${h}</th>`));
      trh.append('<th>操作</th>'); thead.append(trh); table.append(thead);
      const tbody = $('<tbody></tbody>');
      s.rows.forEach(r => {
        const tr = $('<tr></tr>');
        r.values.forEach(v => {
          const cellText = escapeHtml(v);
          const cell = $(`<td contenteditable="true">${cellText}</td>`);
          // highlight matched keyword if present
          const kw = $('#keyword').val() || '';
          if(kw && cellText.toLowerCase().indexOf(kw.toLowerCase())!==-1){ cell.addClass('match'); }
          tr.append(cell);
        });
        const ops = $(`<td>
          <button class="btn btn-sm btn-success save-row">保存</button>
          <button class="btn btn-sm btn-danger del-row">删除</button>
        </td>`);
        tr.append(ops);
        tr.data('row_index', r.row_index);
        tbody.append(tr);
      });
      table.append(tbody);
      body.append(table);
      // pagination controls
      const pager = $(`<div class="mt-2 d-flex align-items-center"><small class="me-2">共 ${s.total} 条</small><div><button class="btn btn-sm btn-outline-secondary prev-page">上一页</button><span class="mx-2 page-info">第 ${s.page} 页</span><button class="btn btn-sm btn-outline-secondary next-page">下一页</button></div></div>`);
      body.append(pager);

      // handlers
      body.on('click', '.save-row', function(){
        const tr = $(this).closest('tr');
        const row_index = tr.data('row_index');
        const values = tr.find('td').not(':last').map(function(){ return $(this).text(); }).get();
        const payload = {filename: filename, sheet: s.sheet, action: 'update', row_index: row_index, values: values};
        fetch('/save_changes', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)}).then(r=>r.json()).then(res=>{
          if(res.status==='ok') alert('保存成功'); else alert('保存失败:'+ (res.error||JSON.stringify(res)));
        }).catch(e=>alert('保存失败'));
      });

      body.on('click', '.del-row', function(){
        if(!confirm('确认删除该记录？')) return;
        const tr = $(this).closest('tr');
        const row_index = tr.data('row_index');
        const payload = {filename: filename, sheet: s.sheet, action: 'delete', row_index: row_index};
        fetch('/save_changes', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)}).then(r=>r.json()).then(res=>{
          if(res.status==='ok'){ tr.remove(); alert('删除成功'); } else alert('删除失败:'+ (res.error||JSON.stringify(res)));
        }).catch(e=>alert('删除失败'));
      });

      body.on('click', '.add-row', function(){
        const headers = s.header;
        const modalEl = document.getElementById('addRowModal');
        const $inputs = $('#addRowModal .modal-body .inputs');
        $inputs.empty();
        headers.forEach(h => {
          const id = 'addcol_' + Math.random().toString(36).slice(2,8);
          $inputs.append(`<div class="mb-3"><label class="form-label">${h}</label><input id="${id}" class="form-control add-row-input" data-col="${h}"/></div>`);
        });
        // store context on modal
        $('#addRowModal').data('sheet', s.sheet).data('filename', filename).data('page_size', s.page_size||20);
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
      });

      // pagination handlers
      body.on('click', '.prev-page', function(){
        const curPage = s.page || 1; if(curPage<=1) return; const newPage = curPage-1;
        const page_size = parseInt($('#pageSize').val()||20);
        doSearch({filename: filename, keyword: $('#keyword').val()||'', sheet: s.sheet, page: newPage, page_size: page_size}, function(res){ if(res && res[0]) replaceSheetCard(s.sheet, res[0], filename); });
      });
      body.on('click', '.next-page', function(){
        const curPage = s.page || 1; const maxPage = Math.ceil((s.total||0)/(s.page_size||20)); if(curPage>=maxPage) return; const newPage = curPage+1;
        const page_size = parseInt($('#pageSize').val()||20);
        doSearch({filename: filename, keyword: $('#keyword').val()||'', sheet: s.sheet, page: newPage, page_size: page_size}, function(res){ if(res && res[0]) replaceSheetCard(s.sheet, res[0], filename); });
      });


      container.append(card);
    });
  }

  function replaceSheetCard(sheetName, s, filename){
    // find existing card for sheet and replace its table+pager
    const container = $('#results');
    const cards = container.find('.card');
    let target = null;
    cards.each(function(){ if($(this).find('h5').first().text()===sheetName) target=$(this); });
    if(!target) return;
    const body = target.find('.card-body');
    // remove old table and pager
    body.find('table').remove(); body.find('.mt-2').remove();
    const table = $('<table class="table table-sm table-bordered"></table>');
    const thead = $('<thead class="table-light"></thead>');
    const trh = $('<tr></tr>');
    s.header.forEach(h => trh.append(`<th>${h}</th>`));
    trh.append('<th>操作</th>'); thead.append(trh); table.append(thead);
    const tbody = $('<tbody></tbody>');
    s.rows.forEach(r => {
      const tr = $('<tr></tr>');
      r.values.forEach(v => tr.append(`<td contenteditable="true">${escapeHtml(v)}</td>`));
      const ops = $(`<td>
        <button class="btn btn-sm btn-success save-row">保存</button>
        <button class="btn btn-sm btn-danger del-row">删除</button>
      </td>`);
      tr.append(ops);
      tr.data('row_index', r.row_index);
      tbody.append(tr);
    });
    table.append(tbody);
    body.append(table);
    const pager = $(`<div class="mt-2 d-flex align-items-center"><small class="me-2">共 ${s.total} 条</small><div><button class="btn btn-sm btn-outline-secondary prev-page">上一页</button><span class="mx-2 page-info">第 ${s.page} 页</span><button class="btn btn-sm btn-outline-secondary next-page">下一页</button></div></div>`);
    body.append(pager);
  }

  // export button
  $('#exportBtn').on('click', function(){
    const filename = $('#fileSelect').val();
    const keyword = $('#keyword').val() || '';
    if(!filename){ alert('请选择文件'); return; }
    // prompt for sheet or empty for all
    // export entire workbook
    const fd = new FormData(); fd.append('filename', filename);
    showLoading('正在导出，请稍候…');
    fetch('/export', {method:'POST', body: fd}).then(r=>{
      if(!r.ok){ alert('导出失败'); hideLoading(); return; }
      return r.blob();
    }).then(blob=>{
      if(!blob){ hideLoading(); return; }
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a'); a.href = url; a.download = `export_${filename}`; document.body.appendChild(a); a.click(); a.remove();
      window.URL.revokeObjectURL(url);
      hideLoading();
    }).catch(e=>{ alert('导出失败'); hideLoading(); });
  });

  // Home button: return to main page (clear results)
  $('#homeBtn').on('click', function(){
    // reload the page to reset state
    window.location.href = '/';
  });

  // add-row modal save handler
  $('#addRowSaveBtn').on('click', function(){
    const modalEl = document.getElementById('addRowModal');
    const $modal = $('#addRowModal');
    const filename = $modal.data('filename');
    const sheet = $modal.data('sheet');
    if(!filename || !sheet){ alert('上下文丢失，请重试'); return; }
    const values = $modal.find('.add-row-input').map(function(){ return $(this).val(); }).get();
    const payload = {filename: filename, sheet: sheet, action: 'add', values: values};
    showLoading('正在保存，请稍候…');
    fetch('/save_changes', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)}).then(r=>r.json()).then(res=>{
      if(res.status==='ok'){
        const modalObj = bootstrap.Modal.getInstance(modalEl);
        if(modalObj) modalObj.hide();
        alert('新增成功');
        // refresh this sheet's first page
        const page_size = parseInt($('#pageSize').val()||20);
        doSearch({filename: filename, keyword: $('#keyword').val()||'', sheet: sheet, page:1, page_size: page_size}, function(result){ if(result && result[0]) replaceSheetCard(sheet, result[0], filename); });
      } else {
        alert('新增失败:'+ (res.error||JSON.stringify(res)));
      }
    }).catch(e=>{ alert('新增失败'); }).finally(()=>{ hideLoading(); });
  });

  function showLoading(text){
    $('#searchBtn').prop('disabled', true);
    $('#exportBtn').prop('disabled', true);
    $('#refreshFiles').prop('disabled', true);
    $('#fileSelect').prop('disabled', true);
    $('#keyword').prop('disabled', true);
    $('#pageSize').prop('disabled', true);
    $('#loadingText').text(text||'处理中...');
    $('#loadingOverlay').removeClass('d-none');
  }
  function hideLoading(){
    $('#searchBtn').prop('disabled', false);
    $('#exportBtn').prop('disabled', false);
    $('#refreshFiles').prop('disabled', false);
    $('#fileSelect').prop('disabled', false);
    $('#keyword').prop('disabled', false);
    $('#pageSize').prop('disabled', false);
    $('#loadingOverlay').addClass('d-none');
  }

  function escapeHtml(text){
    if(!text && text!==0) return '';
    return String(text).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }
});
