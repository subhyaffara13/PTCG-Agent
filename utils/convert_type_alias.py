
def convert_type_alias(self: TypeAlias) -> Json:
    data: Json = {
        ".class": "TypeAlias",
        "fullname": self._fullname,
        "module": self.module,
        "target": convert_type(self.target),
        "alias_tvars": [convert_type(v) for v in self.alias_tvars],
        "no_args": self.no_args,
        "normalized": self.normalized,
        "python_3_12_type_alias": self.python_3_12_type_alias,
    }
    return data

