
def is_uuid(instance: object) -> bool:
    if not isinstance(instance, str):
        return True
    UUID(instance)
    return all(instance[position] == "-" for position in (8, 13, 18, 23))

