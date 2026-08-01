
def tokenize_single_wcomma(val):
    # XXX we match twice the same string (here and at the caller level). It is
    # stupid, but it is easier for now...
    m = r_wcomattrval.match(val)
    if m:
        try:
            name = m.group(1).strip()
            type = m.group(2).strip()
        except IndexError as e:
            raise ValueError("Error while tokenizing attribute") from e
    else:
        raise ValueError(f"Error while tokenizing single {val}")
    return name, type

