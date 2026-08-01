
def convert_param_spec_expr(self: ParamSpecExpr) -> Json:
    return {
        ".class": "ParamSpecExpr",
        "name": self._name,
        "fullname": self._fullname,
        "upper_bound": convert_type(self.upper_bound),
        "default": convert_type(self.default),
        "variance": self.variance,
    }

