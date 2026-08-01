
def right_w_dups(right_no_dup):
    return concat(
        [right_no_dup, DataFrame({"a": ["e"], "c": ["moo"]}, index=[3])]
    ).set_index("a")

