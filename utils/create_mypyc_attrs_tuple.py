
def create_mypyc_attrs_tuple(builder: IRBuilder, ir: ClassIR, line: int) -> Value:
    attrs = [name for ancestor in ir.mro for name in ancestor.attributes]
    if ir.inherits_python:
        attrs.append("__dict__")
    items = [builder.load_str(attr) for attr in attrs]
    return builder.new_tuple(items, line)

