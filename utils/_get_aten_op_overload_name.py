
def _get_aten_op_overload_name(n: _C.Node) -> str:
    # Returns `overload_name` attribute to ATen ops on non-Caffe2 builds
    schema = n.schema()
    if not schema.startswith("aten::"):
        return ""
    return _C.parse_schema(schema).overload_name

