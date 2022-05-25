import java.awt.Color;
import java.awt.Point;
 
import javax.swing.BorderFactory;
import javax.swing.JFrame;
import javax.swing.JLabel;
 
public class guo_ji_xiang_qi_qipan {
 public static void main(String[] args) {
 //JFrame是指一个计算机语言-java的GUI程序的基本思路是
 //Frame为基础，它是屏幕上window的对象，能够最大化、最小化、关闭。
 JFrame f = new JFrame("国际象棋棋盘");
 //窗口大小设置
 f.setSize(168, 195);
 //窗口设置位置
 Point point = new Point(0,0);
 f.setLocation(point);
 
 int grids = 8;
 int gridsSize = 20;
 
 for(int i = 0; i<grids;i++) {
  for(int j = 0; j < grids;j++) {
  //JLable标签属性
  JLabel l = new JLabel();
  l.setSize(gridsSize, gridsSize);
  l.setLocation(i*gridsSize, j*gridsSize);
  if((i + j)%2 == 0) {
   l.setBackground(Color.BLACK);
   //setOpaque让区域内所有像素全部显示为设定颜色
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