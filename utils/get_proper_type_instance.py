
def get_proper_type_instance(ctx: FunctionContext) -> Instance:
    checker = ctx.api
    assert isinstance(checker, TypeChecker)
    types = checker.modules["mypy.types"]
    proper_type_info = types.names["ProperType"]
    assert isinstance(proper_type_info.node, TypeInfo)
    return Instance(proper_type_info.node, [])

