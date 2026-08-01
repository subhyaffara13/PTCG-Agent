
def pprint_thing_encoded(
    object: object, encoding: str = "utf-8", errors: str = "replace"
) -> bytes:
    value = pprint_thing(object)  # get unicode representation of object
    return value.encode(encoding, errors)

