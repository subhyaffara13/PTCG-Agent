
def do_not_convert_to_tracable_parameter() -> Generator[bool, None, None]:
    old_flag = getattr(_TLS, "convert_tracable_parameter", True)
    _TLS.convert_tracable_parameter = False
    try:
        yield False
    finally:
        _TLS.convert_tracable_parameter = old_flag

