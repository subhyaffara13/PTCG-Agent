
def convert_type_info(self: TypeInfo, cfg: Config) -> Json:
    data = {
        ".class": "TypeInfo",
        "module_name": self.module_name,
        "fullname": self.fullname,
        "names": convert_symbol_table(self.names, cfg),
        "defn": convert_class_def(self.defn),
        "abstract_attributes": self.abstract_attributes,
        "type_vars": self.type_vars,
        "has_param_spec_type": self.has_param_spec_type,
        "bases": [convert_type(b) for b in self.bases],
        "mro": self._mro_refs,
        "_promote": [convert_type(p) for p in self._promote],
        "alt_promote": None if self.alt_promote is None else convert_type(self.alt_promote),
        "declared_metaclass": (
            None if self.declared_metaclass is None else convert_type(self.declared_metaclass)
        ),
        "metaclass_type": (
            None if self.metaclass_type is None else convert_type(self.metaclass_type)
        ),
        "tuple_type": None if self.tuple_type is None else convert_type(self.tuple_type),
        "typeddict_type": (
            None if self.typeddict_type is None else convert_typeddict_type(self.typeddict_type)
        ),
        "flags": get_flags(self, TypeInfo.FLAGS),
        "metadata": self.metadata,
        "slots": sorted(self.slots) if self.slots is not None else None,
        "deletable_attributes": self.deletable_attributes,
        "self_type": convert_type(self.self_type) if self.self_type is not None else None,
        "dataclass_transform_spec": (
            convert_dataclass_transform_spec(self.dataclass_transform_spec)
            if self.dataclass_transform_spec is not None
            else None
        ),
        "deprecated": self.deprecated,
    }
    return data

