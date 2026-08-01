
def convert_instance(self: Instance) -> Json:
    ready = self.type is not NOT_READY
    if not self.args and not self.last_known_value and not self.extra_attrs:
        if ready:
            return self.type.fullname
        elif self.type_ref:
            return self.type_ref

    data: dict[str, Any] = {
        ".class": "Instance",
        "type_ref": self.type.fullname if ready else self.type_ref,
        "args": [convert_type(arg) for arg in self.args],
    }
    if self.last_known_value is not None:
        data["last_known_value"] = convert_type(self.last_known_value)
    data["extra_attrs"] = convert_extra_attrs(self.extra_attrs) if self.extra_attrs else None
    return data

