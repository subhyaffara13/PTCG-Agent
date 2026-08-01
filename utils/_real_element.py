
def _real_element(value: float, ctx: SimpleNamespace) -> etree.Element:
    el = etree.Element("real")
    el.text = repr(value)
    return el

