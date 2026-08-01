
def _bool_element(value: bool, ctx: SimpleNamespace) -> etree.Element:
    if value:
        return etree.Element("true")
    return etree.Element("false")

