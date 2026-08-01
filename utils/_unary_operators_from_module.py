
def _unary_operators_from_module() -> dict[type[ast.unaryop], str]:
    return {ast.UAdd: "+", ast.USub: "-", ast.Not: "not", ast.Invert: "~"}

