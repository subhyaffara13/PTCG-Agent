
def convert_class_def(self: ClassDef) -> Json:
    return {
        ".class": "ClassDef",
        "name": self.name,
        "fullname": self.fullname,
        "type_vars": [convert_type(v) for v in self.type_vars],
    }

