
def right_no_dup():
    return DataFrame(
        {
            "a": ["a", "b", "c", "d", "e"],
            "c": ["meow", "bark", "um... weasel noise?", "nay", "chirp"],
        },
        index=range(5),
    ).set_index("a")

