
def _encode_bytes_values(values: dict[bytes, int]) -> list[bytes]:
    value_by_index = {index: value for value, index in values.items()}
    result = []
    line: list[bytes] = []
    line_len = 0
    for i in range(len(values)):
        value = value_by_index[i]
        c_init = format_int(len(value))
        c_len = len(c_init) + len(value)
        if line_len > 0 and line_len + c_len > 70:
            result.append(format_int(len(line)) + b"".join(line))
            line = []
            line_len = 0
        line.append(c_init + value)
        line_len += c_len
    if line:
        result.append(format_int(len(line)) + b"".join(line))
    result.append(b"")
    return result

