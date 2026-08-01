
def write_parse_error(data: WriteBuffer, err: ParseError) -> None:
    write_int(data, err["line"])
    write_int(data, err["column"])
    write_str(data, err["message"])
    if (blocker := err.get("blocker")) is not None:
        write_bool(data, blocker)
    else:
        write_tag(data, LITERAL_NONE)
    write_str_opt(data, err.get("code"))

