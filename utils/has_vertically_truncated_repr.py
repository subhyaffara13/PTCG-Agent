
def has_vertically_truncated_repr(df):
    r = repr(df)
    only_dot_row = False
    for row in r.splitlines():
        if re.match(r"^[\.\ ]+$", row):
            only_dot_row = True
    return only_dot_row

