from typing import Dict

def group_elements_by_id(tree: etree.Element) -> Dict[str, etree.Element]:
    # select all svg elements with 'id' attribute no matter where they are
    # including the root element itself:
    # https://github.com/fonttools/fonttools/issues/2548
    return {el.attrib["id"]: el for el in xpath("//svg:*[@id]")(tree)}

