
def convert_any_type(self: AnyType) -> Json:
    return {
        ".class": "AnyType",
        "type_of_any": self.type_of_any,
        "source_any": convert_type(self.source_any) if self.source_any is not None else None,
        "missing_import_name": self.missing_import_name,
    }

