
def convert_type_var_tuple_type(self: TypeVarTupleType) -> Json:
    assert not self.id.is_meta_var()
    return {
        ".class": "TypeVarTupleType",
        "name": self.name,
        "fullname": self.fullname,
        "id": self.id.raw_id,
        "namespace": self.id.namespace,
        "upper_bound": convert_type(self.upper_bound),
        "tuple_fallback": convert_type(self.tuple_fallback),
        "default": convert_type(self.default),
        "min_len": self.min_len,
    }

