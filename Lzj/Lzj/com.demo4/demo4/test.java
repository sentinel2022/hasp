
import java.util.Scanner;

public class test {

  public static void main(String[] args) {
   /** 1. ����һ����ϵ��
    *2.����ָ������ϵ��
    *3.�������е���ϵ��
    *4. �޸���ϵ����Ϣ
    *5.ɾ����ϵ����Ϣ
    *6.�˳�ϵͳ**/
   PhoneBook phoneBook = new PhoneBook();
    System.out.println("==================�绰��ϵͳ===================");
    Scanner sc =new Scanner(System.in);
   prof: while(true) {

      while (true) {
        System.out.println("---------------------------------------------------------");
        System.out.println("1,�������ϵ�ˡ� 2,��������ϵ�ˡ� 3,��������С�");
        System.out.println("4,���޸���ϵ�ˡ� 5,��ɾ����ϵ�ˡ� 6,���˳�ϵͳ��");
        System.out.println("----------------------------------------------------------");

        System.out.print("ѡ���������š���");
        if(!sc.hasNextInt()){
          sc.next();
          System.out.println("��������,�����¡�����");
          continue ;
        }
        int num = sc.nextInt();
        switch (num) {
          case 1:
            System.out.println("���롾��ӡ�������");
            System.out.println("��Ӳ���");
            System.out.print("����������");String name =sc.next();
            /*������Ա����˼����ƣ��л���Ů�������������Ҳ����жϣ����������Ż�*/
            while(true) {
              System.out.print("�����Ա�");
              String sex = sc.next();
              if (!("��".equals(sex) || "Ů".equals(sex))) {
                System.out.println("�������󣬡����¡�����");
                continue;
              }
              System.out.print("��������: ");Integer age = sc.nextInt();
              System.out.print("����绰���룺");String phoneNo = sc.next();
              System.out.print("����֤���ţ�");String idCard = sc.next();
              phoneBook.addContPerson(name,sex,age,phoneNo,idCard);
              break;
            }
          case 2:
            System.out.println("���롾��ѯ��������");
            System.out.print("������ϵ�ˡ�������");String fname = sc.next();
            ContactPerson[] contactPeoples=phoneBook.findByName(fname);
            if(contactPeoples!=null){
              for(ContactPerson contactPeople : contactPeoples){
                 contactPeople.show();
              }
              System.out.println("��ѯ�ɹ�");
            }else{
              System.out.println("������Ϣ");
            }
            break;

          case 3:
            System.out.println("���롾�����������");
            phoneBook.findAll();
            break;

          case 4:
            System.out.println("���롾�޸ġ�������");
            System.out.print("�����޸ĵġ���š�: ");
            int id =sc.nextInt();
            System.out.print("�����ֻ��š��޸ĳ�: ");
            String newphoneNo = sc.next();
            phoneBook.modfyMesById(id,newphoneNo);
            break;

          case 5:
              System.out.println("���롾ɾ����������");
             while(true) {
              System.out.println("����Ҫɾ���꡾��š�:");
              /*������һ�¼��жϣ����������ſ���*/
              if (!sc.hasNextInt()) {
                System.out.println("�������󣬡����¡�����");
                sc.next();
                continue;
              }
              int delid = sc.nextInt();
              phoneBook.delContPerson(delid);
              break;
            }break;
          case 6:
            System.out.println("�˳��ɹ�");
            break prof;
        }
      }
    }
  }
}