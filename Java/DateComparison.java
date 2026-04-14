import java.util.Date;

public class DateComparison {
    public static void main(String[] args) {
        Date date1 = new Date(2021, 5, 15); // 2021年6月15日
        Date date2 = new Date(2021, 5, 20); // 2021年6月20日
        
        // 使用 before() 方法
        System.out.println("date1 在 date2 之前吗？ " + date1.before(date2));
        
        // 使用 after() 方法
        System.out.println("date1 在 date2 之后吗？ " + date1.after(date2));
        
        // 使用 equals() 方法
        System.out.println("两个日期相同吗？ " + date1.equals(date2));
    }
}