

import java.util.Arrays;

public class PhoneBook {

  private ContactPerson[ ]  contactPersons ;
  private int size;

  public PhoneBook(){
    contactPersons= new ContactPerson[20];
    size=0;
  }

    //1. 新增一个联系人
    public void addContPerson(String name,String sex,int age, String phoneNo, String IdCard){
     ContactPerson person = new ContactPerson(name,sex,age,phoneNo,IdCard);
     contactPersons[size++]= person;
      System.out.println("添加成功");
    }

    // 2.查找指定的联系人
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


    //3.查找所有的联系人
   public void  findAll(){
    for(int i=0; i<size;i++){
      contactPersons[i].show();
    }

   }

   //4. 修改联系人信息
    public void modfyMesById(int id,String phoneNo){

    int i;
    for(i=0; i<size; i++){
      if(contactPersons[i].getId()==id){
        contactPersons[i].setPhoneNo(phoneNo);
        System.out.println("修改成功");
        break;
      }
    }
    if(i>=size){
      System.out.println("修改有误");
    }

 }

    //5.删除联系人信息
    public void delContPerson(int id) {
      int i;
      for(i=0; i<size; i++) {
        if (contactPersons[i].getId() == id) {
          break;
        }
      }
      if(i>=size){
        System.out.println("删除有误");
      }else{
        for(int j=size-2; j>=i; j++){
          contactPersons[j]=contactPersons[j+1];
        }
        size--;
        System.out.println("删除成功");
      }
    }
}