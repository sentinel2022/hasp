import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import Aladdin.Hasp;
import Aladdin.HaspStatus;

public class DOMParserExample {
    public static void main(String[] args) {

long feature = Hasp.HASP_DEFAULT_FID;

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

// hasp.login(vendorCode);

// int status = hasp.getLastError();

// if (HaspStatus.HASP_STATUS_OK != status)
// {
//     /*handle error*/
// }
// System.out.println("ok");


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
}

System.out.println(info);





        try {
            // 创建DocumentBuilderFactory实例
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            // 创建DocumentBuilder实例
            DocumentBuilder builder = factory.newDocumentBuilder();
            // 解析XML文件
            Document document = builder.parse(info);
            
            // 正常化XML结构，使其成为标准的格式
            document.getDocumentElement().normalize();
            
            // 获取包含在<employee>标签中的所有<entry>节点
            NodeList nList = document.getElementsByTagName("entry");
            
            for (int temp = 0; temp < nList.getLength(); temp++) {
                Node node = nList.item(temp);
                
                if (node.getNodeType() == Node.ELEMENT_NODE) {
                    Element element = (Element) node;
                    // 获取<entry>节点中的<key>和<value>子节点
                    String key = element.getElementsByTagName("key").item(0).getTextContent();
                    String value = element.getElementsByTagName("value").item(0).getTextContent();
                    System.out.println("Key: " + key + ", Value: " + value);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
