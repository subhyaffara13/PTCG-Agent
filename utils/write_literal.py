
def write_literal(data: WriteBuffer, value: int | str | bool | float | complex | None) -> None:
    if isinstance(value, bool):
        write_bool(data, value)
    elif isinstance(value, int):
        write_tag(data, LITERAL_INT)
        write_int_bare(data, value)
    elif isinstance(value, str):
        write_tag(data, LITERAL_STR)
        write_str_bare(data, value)
    elif isinstance(value, float):
        write_tag(data, LITERAL_FLOAT)
        write_float_bare(data, value)
    elif isinstance(value, complex):
        write_tag(data, LITERAL_COMPLEX)
        write_float_bare(data, value.real)
        write_float_bare(data, value.imag)
    else:
        write_tag(data, LITERAL_NONE)

