
def left_w_dups(left_no_dup):
    return concat(
        [left_no_dup, DataFrame({"a": ["a"], "b": ["cow"]}, index=[3])], sort=True
    )

