
def _string_element(value: str, ctx: SimpleNamespace) -> etree.Element:
    el = etree.Element("string")
    el.text = value
    return el

