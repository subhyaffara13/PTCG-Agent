
def time():
    """returns the current time in ms of the PortMidi timer
    pygame.midi.time(): return time

    The time is reset to 0, when the module is inited.
    """
    _check_init()
    return _pypm.Time()


def time(raw: str) -> Time:
    """Create a TOML time."""
    value = parse_rfc3339(raw)
    if not isinstance(value, _datetime.time):
        raise ValueError("time() only accepts time strings.")

    return item(value)

