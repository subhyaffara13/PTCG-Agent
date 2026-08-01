
def _has_direct_dataclass_transform_metaclass(info: TypeInfo) -> bool:
    return (
        info.declared_metaclass is not None
        and info.declared_metaclass.type.dataclass_transform_spec is not None
    )

