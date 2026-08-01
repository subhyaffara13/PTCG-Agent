
def format_string_list(lst: list[str]) -> str:
    assert lst
    if len(lst) == 1:
        return lst[0]
    elif len(lst) <= 5:
        return f"{', '.join(lst[:-1])} and {lst[-1]}"
    else:
        return "%s, ... and %s (%i methods suppressed)" % (
            ", ".join(lst[:2]),
            lst[-1],
            len(lst) - 3,
        )

