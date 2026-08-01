
def convert_type_var_tuple_expr(self: TypeVarTupleExpr) -> Json:
    return {
        ".class": "TypeVarTupleExpr",
        "name": self._name,
        "fullname": self._fullname,
        "upper_bound": convert_type(self.upper_bound),
        "tuple_fallback": convert_type(self.tuple_fallback),
        "default": convert_type(self.default),
        "variance": self.variance,
    }

