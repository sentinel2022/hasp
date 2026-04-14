import java.util.Scanner;
 
public class CharInput {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("请输入一个字符:");
        char ch = scanner.next().charAt(0); // 使用next()方法读取一行文本，然后取第一个字符
        System.out.println("你输入的字符是: " + ch);
        scanner.close(); // 关闭scanner对象
    }
}