
def _make_element(value: PlistEncodable, ctx: SimpleNamespace) -> etree.Element:
    raise TypeError("unsupported type: %s" % type(value))

