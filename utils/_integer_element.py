
def _integer_element(value: int, ctx: SimpleNamespace) -> etree.Element:
    if -1 << 63 <= value < 1 << 64:
        el = etree.Element("integer")
        el.text = "%d" % value
        return el
    raise OverflowError(value)

