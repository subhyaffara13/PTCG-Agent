
def process_split(config, items):
    split = config.getoption("--split")
    if not split:
        return
    m = sp.match(split)
    if not m:
        raise ValueError(
            "split must be a string of the form a/b " "where a and b are ints."
        )
    i, t = map(int, m.groups())
    start, end = (i - 1) * len(items) // t, i * len(items) // t

    if i < t:
        # remove elements from end of list first
        del items[end:]
    del items[:start]

