
def convert_overloaded_func_def(self: OverloadedFuncDef) -> Json:
    return {
        ".class": "OverloadedFuncDef",
        "items": [convert_overload_part(i) for i in self.items],
        "type": None if self.type is None else convert_type(self.type),
        "fullname": self._fullname,
        "impl": None if self.impl is None else convert_overload_part(self.impl),
        "flags": get_flags(self, FUNCBASE_FLAGS),
        "deprecated": self.deprecated,
        "setter_index": self.setter_index,
    }

