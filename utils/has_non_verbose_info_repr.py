
def has_non_verbose_info_repr(df):
    has_info = has_info_repr(df)
    r = repr(df)

    # 1. <class>
    # 2. Index
    # 3. Columns
    # 4. dtype
    # 5. memory usage
    # 6. trailing newline
    nv = len(r.split("\n")) == 6
    return has_info and nv

