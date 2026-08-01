
def convert_param_spec_type(self: ParamSpecType) -> Json:
    assert not self.id.is_meta_var()
    return {
        ".class": "ParamSpecType",
        "name": self.name,
        "fullname": self.fullname,
        "id": self.id.raw_id,
        "namespace": self.id.namespace,
        "flavor": self.flavor,
        "upper_bound": convert_type(self.upper_bound),
        "default": convert_type(self.default),
        "prefix": convert_type(self.prefix),
    }

