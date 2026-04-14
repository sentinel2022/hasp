
import java.util.Scanner;

public class ProgramRouter {
    public static void main(String[] args) {
       
        Scanner scanner = new Scanner(System.in);
        
        while (true) {
            System.out.print("请输入指令(help/calc/game/exit): ");
            String input = scanner.nextLine().trim().toLowerCase();
            
            switch (input) {
                case "help":
                    showHelp();
                    break;
                case "calc":
                    runCalculator();
                    break;
                case "game":
                    startGame();
                    break;
                case "exit":
                    System.exit(0);
                    break;
                default:
                    System.out.println("未知指令，输入help查看帮助");
            }
        }
    }

    private static void showHelp() {
        System.out.println("=== 帮助菜单 ===");
        System.out.println("help - 显示本帮助");
        System.out.println("calc - 启动计算器");
        System.out.println("game - 启动小游戏");
        System.out.println("exit - 退出程序");
    }

    private static void runCalculator() {
        System.out.println(">>> 计算器功能待实现");
    }

    private static void startGame() {
        System.out.println(">>> 游戏功能待实现");
    }
}
