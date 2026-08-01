
def get_original_any(t: AnyType) -> AnyType:
    if t.type_of_any == TypeOfAny.from_another_any:
        assert t.source_any
        assert t.source_any.type_of_any != TypeOfAny.from_another_any
        t = t.source_any
    return t

