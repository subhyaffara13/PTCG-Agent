
def _format_possibilities(possibilities: list[str]) -> str:
    possibility_str = ", ".join(repr(p) for p in sorted(possibilities))
    return ngettext(
        "Did you mean {possibility}?",
        "(Did you mean one of: {possibilities}?)",
        len(possibilities),
    ).format(possibility=possibility_str, possibilities=possibility_str)

