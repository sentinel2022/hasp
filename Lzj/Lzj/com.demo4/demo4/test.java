
import java.util.Scanner;

public class test {

  public static void main(String[] args) {
   /** 1. 新增一个联系人
    *2.查找指定的联系人
    *3.查找所有的联系人
    *4. 修改联系人信息
    *5.删除联系人信息
    *6.退出系统**/
   PhoneBook phoneBook = new PhoneBook();
    System.out.println("==================电话本系统===================");
    Scanner sc =new Scanner(System.in);
   prof: while(true) {

      while (true) {
        System.out.println("---------------------------------------------------------");
        System.out.println("1,【添加联系人】 2,【查找联系人】 3,【浏览所有】");
        System.out.println("4,【修改联系人】 5,【删除联系人】 6,【退出系统】");
        System.out.println("----------------------------------------------------------");

        System.out.print("选择操作【标号】：");
        if(!sc.hasNextInt()){
          sc.next();
          System.out.println("输入有序,【重新】输入");
          continue ;
        }
        int num = sc.nextInt();
        switch (num) {
          case 1:
            System.out.println("进入【添加】操作：");
            System.out.println("添加操作");
            System.out.print("输入姓名：");String name =sc.next();
            /*这里对性别做了简单限制，男或者女，其他输入暂且不做判断，可以自行优化*/
            while(true) {
              System.out.print("输入性别：");
              String sex = sc.next();
              if (!("男".equals(sex) || "女".equals(sex))) {
                System.out.println("输入有误，【重新】输入");
                continue;
              }
              System.out.print("输入年龄: ");Integer age = sc.nextInt();
              System.out.print("输入电话号码：");String phoneNo = sc.next();
              System.out.print("输入证件号：");String idCard = sc.next();
              phoneBook.addContPerson(name,sex,age,phoneNo,idCard);
              break;
            }
          case 2:
            System.out.println("进入【查询】操作：");
            System.out.print("输入联系人【姓名】");String fname = sc.next();
            ContactPerson[] contactPeoples=phoneBook.findByName(fname);
            if(contactPeoples!=null){
              for(ContactPerson contactPeople : contactPeoples){
                 contactPeople.show();
              }
              System.out.println("查询成功");
            }else{
              System.out.println("暂无信息");
            }
            break;

          case 3:
            System.out.println("进入【浏览】操作：");
            phoneBook.findAll();
            break;

          case 4:
            System.out.println("进入【修改】操作：");
            System.out.print("输入修改的【标号】: ");
            int id =sc.nextInt();
            System.out.print("将【手机号】修改成: ");
            String newphoneNo = sc.next();
            phoneBook.modfyMesById(id,newphoneNo);
            break;

          case 5:
              System.out.println("进入【删除】操作：");
             while(true) {
              System.out.println("输入要删除标【标号】:");
              /*这里做一下简单判断，输入整数才可以*/
              if (!sc.hasNextInt()) {
                System.out.println("输入有误，【重新】输入");
                sc.next();
                continue;
              }
              int delid = sc.nextInt();
              phoneBook.delContPerson(delid);
              break;
            }break;
          case 6:
            System.out.println("退出成功");
            break prof;
        }
      }
    }
  }
}