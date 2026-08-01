
def write_json_value(data: WriteBuffer, value: JsonValue) -> None:
    if value is None:
        write_tag(data, LITERAL_NONE)
    elif isinstance(value, bool):
        write_bool(data, value)
    elif isinstance(value, int):
        write_tag(data, LITERAL_INT)
        write_int_bare(data, value)
    elif isinstance(value, str):
        write_tag(data, LITERAL_STR)
        write_str_bare(data, value)
    elif isinstance(value, list):
        write_tag(data, LIST_GEN)
        write_int_bare(data, len(value))
        for val in value:
            write_json_value(data, val)
    elif isinstance(value, tuple):
        write_tag(data, TUPLE_GEN)
        write_int_bare(data, len(value))
        for val in value:
            write_json_value(data, val)
    elif isinstance(value, dict):
        write_tag(data, DICT_STR_GEN)
        write_int_bare(data, len(value))
        for key in sorted(value):
            write_str_bare(data, key)
            write_json_value(data, value[key])
    elif isinstance(value, float):
        write_tag(data, LITERAL_FLOAT)
        write_float_bare(data, value)
    else:
        assert False, f"Invalid JSON value: {value}"

