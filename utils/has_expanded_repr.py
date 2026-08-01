
def has_expanded_repr(df):
    r = repr(df)
    for line in r.split("\n"):
        if line.endswith("\\"):
            return True
    return False

