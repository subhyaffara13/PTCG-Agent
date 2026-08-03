import re

def sanitize_pytest_xml(xml_file: str):
    # pytext xml is different from unittext xml, this function makes pytest xml more similar to unittest xml
    # consider somehow modifying the XML logger in conftest to do this instead
    import xml.etree.ElementTree as ET
    tree = ET.parse(xml_file)
    for testcase in tree.iter('testcase'):
        full_classname = testcase.attrib.get("classname")
        if full_classname is None:
            continue
        # The test prefix is optional
        regex_result = re.search(r"^(test\.)?(?P<file>.*)\.(?P<classname>[^\.]*)$", full_classname)
        if regex_result is None:
            continue
        classname = regex_result.group("classname")
        file = regex_result.group("file").replace(".", "/")
        testcase.set("classname", classname)
        testcase.set("file", f"{file}.py")
    tree.write(xml_file)

