
def convert_func_def(self: FuncDef) -> Json:
    return {
        ".class": "FuncDef",
        "name": self._name,
        "fullname": self._fullname,
        "arg_names": self.arg_names,
        "arg_kinds": [int(x.value) for x in self.arg_kinds],
        "type": None if self.type is None else convert_type(self.type),
        "flags": get_flags(self, FUNCDEF_FLAGS),
        "abstract_status": self.abstract_status,
        # TODO: Do we need expanded, original_def?
        "dataclass_transform_spec": (
            None
            if self.dataclass_transform_spec is None
            else convert_dataclass_transform_spec(self.dataclass_transform_spec)
        ),
        "deprecated": self.deprecated,
        "original_first_arg": self.original_first_arg,
    }

