
def object_has_getattribute(value: Any) -> bool:
    return class_has_getattribute(type(value))

