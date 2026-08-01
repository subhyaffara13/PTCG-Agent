
def _bool_operators_from_module() -> dict[type[ast.boolop], str]:
    return {ast.And: "and", ast.Or: "or"}

