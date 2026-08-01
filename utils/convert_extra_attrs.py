
def convert_extra_attrs(self: ExtraAttrs) -> Json:
    return {
        ".class": "ExtraAttrs",
        "attrs": {k: convert_type(v) for k, v in self.attrs.items()},
        "immutable": sorted(self.immutable),
        "mod_name": self.mod_name,
    }

