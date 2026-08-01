
def convert_type_alias_type(self: TypeAliasType) -> Json:
    data: Json = {
        ".class": "TypeAliasType",
        "type_ref": self.type_ref,
        "args": [convert_type(arg) for arg in self.args],
    }
    return data

