import java.awt.Color;
import java.awt.Point;
 
import javax.swing.BorderFactory;
import javax.swing.JFrame;
import javax.swing.JLabel;
 
public class guo_ji_xiang_qi_qipan {
 public static void main(String[] args) {
 //JFrame��ָһ�����������-java��GUI����Ļ���˼·��
 //FrameΪ������������Ļ��window�Ķ����ܹ���󻯡���С�����رա�
 JFrame f = new JFrame("������������");
 //���ڴ�С����
 f.setSize(168, 195);
 //��������λ��
 Point point = new Point(0,0);
 f.setLocation(point);
 
 int grids = 8;
 int gridsSize = 20;
 
 for(int i = 0; i<grids;i++) {
  for(int j = 0; j < grids;j++) {
  //JLable��ǩ����
  JLabel l = new JLabel();
  l.setSize(gridsSize, gridsSize);
  l.setLocation(i*gridsSize, j*gridsSize);
  if((i + j)%2 == 0) {
   l.setBackground(Color.BLACK);
   //setOpaque����������������ȫ����ʾΪ�趨��ɫ
   l.setOpaque(true);
  }else {
   l.setBackground(Color.white);
   l.setOpaque(true);
  }
  l.setBorder(BorderFactory.createLineBorder(Color.BLACK));
  
  f.add(l);
  
  }
 }
 f.setVisible(true);
 }
 
}