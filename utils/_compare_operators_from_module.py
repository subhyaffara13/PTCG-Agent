
def _compare_operators_from_module() -> dict[type[ast.cmpop], str]:
    return {
        ast.Eq: "==",
        ast.Gt: ">",
        ast.GtE: ">=",
        ast.In: "in",
        ast.Is: "is",
        ast.IsNot: "is not",
        ast.Lt: "<",
        ast.LtE: "<=",
        ast.NotEq: "!=",
        ast.NotIn: "not in",
    }

