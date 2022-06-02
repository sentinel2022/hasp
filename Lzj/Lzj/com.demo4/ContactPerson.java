package com.demo4;

/**1������һ����ϵ�ˣ���ϵ�˵ı�Ŵ�1��ʼ�Զ��������������Ա����䣬�ֻ��ţ�
 ���֤�����û��ӿ���̨¼��*/
public class ContactPerson {

  /*�����þ�̬��ʶ��diΪ������*/
  private static int  count=0;

  private int id;
  private String name;
  private String sex;
  private int age;
  private String phoneNo;
  private String IdCard;

  public ContactPerson(){}

  public ContactPerson(String name, String sex, int age, String phoneNo, String idCard) {
      this.name = name;
      this.sex = sex;
      this.age = age;
      this.phoneNo = phoneNo;
      IdCard = idCard;
      /*��̬idΪ������*/
      this.id = ++count;
  }

  public int getId() {
    return id;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getSex() {
    return sex;
  }

  public void setSex(String sex) {
    this.sex = sex;
  }

  public int getAge() {
    return age;
  }

  public void setAge(int age) {
    this.age = age;
  }

  public String getPhoneNo() {
    return phoneNo;
  }

  public void setPhoneNo(String phoneNo) {
    this.phoneNo = phoneNo;
  }

  public String getIdCard() {
    return IdCard;
  }

  public void setIdCard(String idCard) {
    IdCard = idCard;
  }

  public static int getCount() {
    return count;
  }

  public void show() {
    System.out.println(
       "�� ��� =" + id + " ����=" + name + ", �Ա�=" + sex + ", ����=" + age + ", �绰����=" + phoneNo + ", ֤����=" + IdCard +" ��" );
   }


}