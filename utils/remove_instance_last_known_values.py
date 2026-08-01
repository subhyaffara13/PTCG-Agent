
def remove_instance_last_known_values(t: Type) -> Type:
    return t.accept(LastKnownValueEraser())

