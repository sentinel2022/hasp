import Aladdin.HaspStatus;
import Aladdin.Hasp;

 
public class GetInfo {
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

System.out.println("raw xml info:\n" + info);

if (info != null && !info.trim().isEmpty()) {
    parseAndPrintHaspInfo(info);
} else {
    System.out.println("No XML info returned to parse.");
}

}

private static void parseAndPrintHaspInfo(String xml) {
    String haspId = "";
    String haspType = "";

    try {
        javax.xml.parsers.DocumentBuilderFactory factory = javax.xml.parsers.DocumentBuilderFactory.newInstance();
        factory.setNamespaceAware(false);
        javax.xml.parsers.DocumentBuilder builder = factory.newDocumentBuilder();
        org.w3c.dom.Document doc = builder.parse(new org.xml.sax.InputSource(new java.io.StringReader(xml)));

        javax.xml.xpath.XPath xpath = javax.xml.xpath.XPathFactory.newInstance().newXPath();
        haspId = xpath.evaluate("/hasp_info/hasp/@id", doc);
        haspType = xpath.evaluate("/hasp_info/hasp/@type", doc);

        System.out.println("Parsed hasp info:");
        System.out.println("  hasp.id = " + (haspId == null || haspId.isEmpty() ? "<not found>" : haspId));
        System.out.println("  hasp.type = " + (haspType == null || haspType.isEmpty() ? "<not found>" : haspType));

        org.w3c.dom.NodeList features = (org.w3c.dom.NodeList) xpath.evaluate("/hasp_info/hasp/feature", doc, javax.xml.xpath.XPathConstants.NODESET);
        for (int i = 0; i < features.getLength(); i++) {
            org.w3c.dom.Node feature = features.item(i);
            String featureId = xpath.evaluate("@id", feature);
            System.out.printf("  feature[%d].id = %s%n", i, featureId == null || featureId.isEmpty() ? "<not found>" : featureId);
        }

    } catch (Exception ex) {
        System.out.println("Failed to parse XML info: " + ex.getMessage());
        ex.printStackTrace(System.out);
    }

    // 这里用常量调用 equals 防止 haspId 为 null 时 NPE
    if (!"1470921956".equals(haspId)) {
        System.out.println("Unexpected hasp.id value: " + haspId);
    }
    else {
        System.out.println("hasp.id value is correct.");
    }

    System.out.println("程序结束。");
}
}