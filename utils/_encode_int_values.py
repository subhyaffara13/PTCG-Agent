
def _encode_int_values(values: dict[int, int]) -> list[bytes]:
    """Encode int values into C strings.

    Values are stored in base 10 and separated by 0 bytes.
    """
    value_by_index = {index: value for value, index in values.items()}
    result = []
    line: list[bytes] = []
    line_len = 0
    for i in range(len(values)):
        value = value_by_index[i]
        encoded = b"%d" % value
        if line_len > 0 and line_len + len(encoded) > 70:
            result.append(format_int(len(line)) + b"\0".join(line))
            line = []
            line_len = 0
        line.append(encoded)
        line_len += len(encoded)
    if line:
        result.append(format_int(len(line)) + b"\0".join(line))
    result.append(b"")
    return result

