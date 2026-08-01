
def read_parse_error(data: ReadBuffer) -> ParseError:
    err: ParseError = {"line": read_int(data), "column": read_int(data), "message": read_str(data)}
    tag = read_tag(data)
    if tag == LITERAL_TRUE:
        err["blocker"] = True
    elif tag == LITERAL_FALSE:
        err["blocker"] = False
    else:
        assert tag == LITERAL_NONE
    if (code := read_str_opt(data)) is not None:
        err["code"] = code
    return err

