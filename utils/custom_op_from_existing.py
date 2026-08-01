
def custom_op_from_existing(op):
    ns = op.namespace
    lib = torch.library.Library(ns, "FRAGMENT")
    name = op.name().split("::")[-1]
    schema_str = str(op._schema)
    # CustomOp expects the schema string without the namespace
    schema_str = schema_str.rsplit("::", maxsplit=1)[-1]
    schema = FunctionSchema.parse(schema_str)
    return CustomOp(lib, ns, schema, name, op, _private_access=True)

