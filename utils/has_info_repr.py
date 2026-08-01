
def has_info_repr(df):
    r = repr(df)
    c1 = r.split("\n")[0].startswith("<class")
    c2 = r.split("\n")[0].startswith(r"&lt;class")  # _repr_html_
    return c1 or c2

