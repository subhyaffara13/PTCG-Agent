
def get_partial_instance_type(t: Type | None) -> PartialType | None:
    if t is None or not isinstance(t, PartialType) or t.type is None:
        return None
    return t

