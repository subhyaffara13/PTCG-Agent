
def convert_type_var_type(self: TypeVarType) -> Json:
    assert not self.id.is_meta_var()
    return {
        ".class": "TypeVarType",
        "name": self.name,
        "fullname": self.fullname,
        "id": self.id.raw_id,
        "namespace": self.id.namespace,
        "values": [convert_type(v) for v in self.values],
        "upper_bound": convert_type(self.upper_bound),
        "default": convert_type(self.default),
        "variance": self.variance,
    }

