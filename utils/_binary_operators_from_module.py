
def _binary_operators_from_module() -> dict[type[ast.operator], str]:
    return {
        ast.Add: "+",
        ast.BitAnd: "&",
        ast.BitOr: "|",
        ast.BitXor: "^",
        ast.Div: "/",
        ast.FloorDiv: "//",
        ast.MatMult: "@",
        ast.Mod: "%",
        ast.Mult: "*",
        ast.Pow: "**",
        ast.Sub: "-",
        ast.LShift: "<<",
        ast.RShift: ">>",
    }

