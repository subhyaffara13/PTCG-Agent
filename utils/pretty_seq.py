
def pretty_seq(args: Sequence[str], conjunction: str) -> str:
    quoted = ['"' + a + '"' for a in args]
    if len(quoted) == 1:
        return quoted[0]
    if len(quoted) == 2:
        return f"{quoted[0]} {conjunction} {quoted[1]}"
    last_sep = ", " + conjunction + " "
    return ", ".join(quoted[:-1]) + last_sep + quoted[-1]

