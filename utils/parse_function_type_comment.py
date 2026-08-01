
def parse_function_type_comment(type_comment: str) -> FunctionType | None:
    """Given a correct type comment, obtain a FunctionType object."""
    func_type = ast.parse(type_comment, "<type_comment>", "func_type")
    return FunctionType(argtypes=func_type.argtypes, returns=func_type.returns)

