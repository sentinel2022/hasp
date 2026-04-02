// See https://aka.ms/new-console-template for more information
using System.Threading.Tasks;
using Aladdin.HASP;
//using System.Windows.Forms;
using System;
using System.Text;

Console.WriteLine("Hello, 2025---World!");


HaspFeature feature = HaspFeature.FromFeature(0);

string vendorCode =
"AzIceaqfA1hX5wS+M8cGnYh5ceevUnOZIzJBbXFD6dgf3tBkb9cvUF/Tkd/iKu2fsg9wAysYKw7RMAsV" +
"vIp4KcXle/v1RaXrLVnNBJ2H2DmrbUMOZbQUFXe698qmJsqNpLXRA367xpZ54i8kC5DTXwDhfxWTOZrB" +
"rh5sRKHcoVLumztIQjgWh37AzmSd1bLOfUGI0xjAL9zJWO3fRaeB0NS2KlmoKaVT5Y04zZEc06waU2r6" +
"AU2Dc4uipJqJmObqKM+tfNKAS0rZr5IudRiC7pUwnmtaHRe5fgSI8M7yvypvm+13Wm4Gwd4VnYiZvSxf" +
"8ImN3ZOG9wEzfyMIlH2+rKPUVHI+igsqla0Wd9m7ZUR9vFotj1uYV0OzG7hX0+huN2E/IdgLDjbiapj1" +
"e2fKHrMmGFaIvI6xzzJIQJF9GiRZ7+0jNFLKSyzX/K3JAyFrIPObfwM+y+zAgE1sWcZ1YnuBhICyRHBh" +
"aJDKIZL8MywrEfB2yF+R3k9wFG1oN48gSLyfrfEKuB/qgNp+BeTruWUk0AwRE9XVMUuRbjpxa4YA67SK" +
"unFEgFGgUfHBeHJTivvUl0u4Dki1UKAT973P+nXy2O0u239If/kRpNUVhMg8kpk7s8i6Arp7l/705/bL" +
"Cx4kN5hHHSXIqkiG9tHdeNV8VYo5+72hgaCx3/uVoVLmtvxbOIvo120uTJbuLVTvT8KtsOlb3DxwUrwL" +
"zaEMoAQAFk6Q9bNipHxfkRQER4kR7IYTMzSoW5mxh3H9O8Ge5BqVeYMEW36q9wnOYfxOLNw6yQMf8f9s" +
"JN4KhZty02xm707S7VEfJJ1KNq7b5pP/3RjE0IKtB2gE6vAPRvRLzEohu0m7q1aUp8wAvSiqjZy7FLaT" +
"tLEApXYvLvz6PEJdj4TegCZugj7c8bIOEqLXmloZ6EgVnjQ7/ttys7VFITB3mazzFiyQuKf4J6+b/a/Y";

Hasp hasp = new Hasp(feature);
HaspStatus status = hasp.Login(vendorCode);

if (HaspStatus.StatusOk != status)
{
    //handle error
    Console.WriteLine("Error");
    System.Console.WriteLine();
}
else
System.Console.WriteLine("suceess!!!已登录加密锁，功能为0");


//write memory//

HaspFile file1 = hasp.GetFile(HaspFileId.ReadWrite);
Console.WriteLine("Input: ");
string data1 = Console.ReadLine();
Console.WriteLine("data1  :" + data1);
byte[] data2= Encoding.UTF8.GetBytes(data1);

status = file1.Write(data2, 0, data1.Length);

if (HaspStatus.StatusOk != status)
{
    //handle error
}


//read memory
HaspFile file = hasp.GetFile(HaspFileId.ReadWrite);
int size = 48;
byte[] data = new byte[size];
status = file.Read(data, 0, data.Length);

if (HaspStatus.StatusOk != status)
{
    //handle error
    Console.WriteLine("内存读取失败： " + status);
    Console.ReadLine();
    Environment.Exit(0);
}
else
    Console.WriteLine(data);

    string str = System.Text.Encoding.Default.GetString(data);

Console.WriteLine("内存数据为： "+str);

    Console.ReadLine();

