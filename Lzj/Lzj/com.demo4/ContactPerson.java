package com.demo4;

/**1、新增一个联系人，联系人的编号从1开始自动增长，姓名，性别，年龄，手机号，
 身份证号由用户从控制台录入*/
public class ContactPerson {

  /*这里用静态标识，di为自增长*/
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
      /*静态id为自增长*/
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
       "【 编号 =" + id + " 姓名=" + name + ", 性别=" + sex + ", 年龄=" + age + ", 电话号码=" + phoneNo + ", 证件号=" + IdCard +" 】" );
   }


}