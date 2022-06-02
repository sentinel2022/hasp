

import java.util.Arrays;

public class PhoneBook {

  private ContactPerson[ ]  contactPersons ;
  private int size;

  public PhoneBook(){
    contactPersons= new ContactPerson[20];
    size=0;
  }

    //1. ����һ����ϵ��
    public void addContPerson(String name,String sex,int age, String phoneNo, String IdCard){
     ContactPerson person = new ContactPerson(name,sex,age,phoneNo,IdCard);
     contactPersons[size++]= person;
      System.out.println("��ӳɹ�");
    }

    // 2.����ָ������ϵ��
  public ContactPerson[] findByName(String name){

    ContactPerson[] newContPersons = new ContactPerson[size];
    int length=0;

    int i;
    for(i=0; i<size; i++){
      if(contactPersons[i].getName().equals(name)){
        newContPersons[length++] =contactPersons[i];
      }
      i++;
    }

    newContPersons = Arrays.copyOf(newContPersons,length);
    return newContPersons;
  }


    //3.�������е���ϵ��
   public void  findAll(){
    for(int i=0; i<size;i++){
      contactPersons[i].show();
    }

   }

   //4. �޸���ϵ����Ϣ
    public void modfyMesById(int id,String phoneNo){

    int i;
    for(i=0; i<size; i++){
      if(contactPersons[i].getId()==id){
        contactPersons[i].setPhoneNo(phoneNo);
        System.out.println("�޸ĳɹ�");
        break;
      }
    }
    if(i>=size){
      System.out.println("�޸�����");
    }

 }

    //5.ɾ����ϵ����Ϣ
    public void delContPerson(int id) {
      int i;
      for(i=0; i<size; i++) {
        if (contactPersons[i].getId() == id) {
          break;
        }
      }
      if(i>=size){
        System.out.println("ɾ������");
      }else{
        for(int j=size-2; j>=i; j++){
          contactPersons[j]=contactPersons[j+1];
        }
        size--;
        System.out.println("ɾ���ɹ�");
      }
    }
}