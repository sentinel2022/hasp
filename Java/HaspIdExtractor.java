
import Aladdin.Hasp;
import Aladdin.HaspStatus;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import java.io.ByteArrayInputStream;
import java.io.InputStream;



public class HaspIdExtractor {
    public static void main(String[] args) {


//login
//long feature = Hasp.HASP_DEFAULT_FID;
long feature = 0;

String vendorCode = 
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

hasp.login(vendorCode);

int status = hasp.getLastError();

if (HaspStatus.HASP_STATUS_OK != status)
{
    /*handle error*/
    System.out.println("错误代码： "+status);
}
else
{
   System.out.println("OK   !  "+status);
}

      //getinfo
String scope = 
"<?xml version=\"1.0\" encoding=\"UTF-8\" ?>" + 
"<haspscope/>";

String format = 
"<?xml version=\"1.0\" encoding=\"UTF-8\" ?>" + 
"<haspformat root=\"hasp_info\">" + 
"    <hasp>" + 
"        <attribute name=\"id\" />" + 
"        <attribute name=\"type\" />" + 
"        <feature>" + 
"            <attribute name=\"id\" />" + 
"        </feature>" + 
"    </hasp>" + 
"</haspformat>";

String info;

info = hasp.getInfo(scope, format, vendorCode);

int status2 = hasp.getLastError();

if (HaspStatus.HASP_STATUS_OK != status2)
{
    /*handle error*/
    System.out.println("没有发现Key!"+status2);
    return;
}
System.out.println("无需登录锁，获取到Key信息!"+status2);

        try {
            // 创建解析器工厂
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            
            // 将字符串转换为输入流
            InputStream inputStream = new ByteArrayInputStream(info.getBytes("UTF-8"));
            
            // 解析XML数据
            Document doc = builder.parse(inputStream);
            doc.getDocumentElement().normalize();
            
            // 获取hasp元素列表
            NodeList haspList = doc.getElementsByTagName("hasp");
            if (haspList.getLength() > 0) {

                Element haspElement = (Element) haspList.item(0);
                // 提取id属性值
                String haspId = haspElement.getAttribute("id");
                System.out.println("提取的hasp id值: " + haspId);
            } else {
                System.out.println("未找到hasp元素");
            }

            // 获取feature元素列表
            NodeList featureList = doc.getElementsByTagName("feature");
            if (featureList.getLength() > 0) {

                    for (int i = 0; i < featureList.getLength(); i++) {

                Element featureElement = (Element) featureList.item(i);
                // 提取id属性值
                String featureId = featureElement.getAttribute("id");
                System.out.println("提取的feature id值: " + featureId);
                    }}
            else {
                System.out.println("未找到feature元素");
               }
                 
        } catch (Exception e) {
            e.printStackTrace();
        }
//getSessionInfo

String info2;

info2 = hasp.getSessionInfo(Hasp.HASP_SESSIONINFO);

int status3 = hasp.getLastError();

if (HaspStatus.HASP_STATUS_OK != status3)
{
    /*handle error*/
    System.out.println("没有发现Key或没有登录Key!"+status3);
    return;
}
System.out.println("获取到Session信息!"+status3);

   try {
            // 创建解析器工厂
            DocumentBuilderFactory factory2 = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder2 = factory2.newDocumentBuilder();
            
            // 将字符串转换为输入流
            InputStream inputStream2 = new ByteArrayInputStream(info2.getBytes("UTF-8"));
            
            // 解析XML数据
            Document doc2 = builder2.parse(inputStream2);
            doc2.getDocumentElement().normalize();
            
            // 获取feature元素列表
            NodeList feature2List = doc2.getElementsByTagName("license");
            if (feature2List.getLength() > 0) {

                Element feature2Element = (Element) feature2List.item(0);
                // 提取id属性值
                //String feature2Id = feature2Element.getAttribute("featureid");//本行是提取下级的信息

                String feature2Id = feature2Element.getTextContent();

                System.out.println("提取的Session 值: " + feature2Id);
            } else {
                System.out.println("未找到Session元素");
            }

            // 获取feature元素列表
            NodeList feature3List = doc2.getElementsByTagName("concurrency");
            if (feature3List.getLength() > 0) {

                    for (int i = 0; i < feature3List.getLength(); i++) {

                Element feature3Element = (Element) feature3List.item(i);
                // 提取id属性值
                //String feature3Id = feature3Element.getAttribute("export");
                String feature3Id = feature3Element.getTextContent();
                System.out.println("提取的Session 第二个值: " + feature3Id);
                    }}
            else {
                System.out.println("未找到Session第二个元素");
               }
            
        

        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
