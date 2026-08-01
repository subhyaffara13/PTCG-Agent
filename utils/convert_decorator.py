
def convert_decorator(self: Decorator) -> Json:
    return {
        ".class": "Decorator",
        "func": convert_func_def(self.func),
        "var": convert_var(self.var),
        "is_overload": self.is_overload,
    }

