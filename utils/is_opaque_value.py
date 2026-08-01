
def is_opaque_value(value: object) -> TypeIs[OpaqueType]:
    return is_opaque_type(type(value))

