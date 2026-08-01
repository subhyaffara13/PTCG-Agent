
def convert_unbound_type(self: UnboundType) -> Json:
    return {
        ".class": "UnboundType",
        "name": self.name,
        "args": [convert_type(a) for a in self.args],
        "expr": self.original_str_expr,
        "expr_fallback": self.original_str_fallback,
    }

