
def update_special_changes(s, l, t):
    if t[0] == "indentedBlock":
        warnings.warn(
            "Conversion of 'indentedBlock' to new 'IndentedBlock'"
            " requires added code changes to remove 'indentStack' argument\n"
            f"  {pp.lineno(l, s)}: {pp.line(l, s)}",
            stacklevel=2,
        )
    elif t[0] == "locatedExpr":
        warnings.warn(
            "Conversion of 'locatedExpr' to new 'Located'"
            " may require added code changes - Located does not automatically"
            " group parsed elements\n"
            f"  {pp.lineno(l, s)}: {pp.line(l, s)}",
            stacklevel=2,
        )
    return special_changes[t[0]]

