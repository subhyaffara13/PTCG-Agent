
def has_kwarg_only_args(schema: _C.FunctionSchema):
    return any(a.kwarg_only for a in schema.arguments)

