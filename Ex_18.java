修改下,518修改了
519上午修改

public class Ex_18
{
  public static void main(String[] args){
     int j,i,p=1;
     for(i=1;i<=5;i++)
     {
       for(p=1,j=1;j<=5;j++)
       if(i<=5-j)
       System.out.print(" ");
       else
       System.out.print(p++);
System.out.print("\n");
     }
    }
}