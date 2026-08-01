
def c_string_array_initializer(components: list[bytes]) -> str:
    result = []
    result.append("{\n")
    for s in components:
        result.append("    " + c_string_initializer(s) + ",\n")
    result.append("}")
    return "".join(result)

