
def convert_type_var_expr(self: TypeVarExpr) -> Json:
    return {
        ".class": "TypeVarExpr",
        "name": self._name,
        "fullname": self._fullname,
        "values": [convert_type(t) for t in self.values],
        "upper_bound": convert_type(self.upper_bound),
        "default": convert_type(self.default),
        "variance": self.variance,
    }

