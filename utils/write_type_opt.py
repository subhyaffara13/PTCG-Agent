
def write_type_opt(data: WriteBuffer, value: Type | None) -> None:
    if value is not None:
        value.write(data)
    else:
        write_tag(data, LITERAL_NONE)

