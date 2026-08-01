
def _expand_elements(body) -> None:
    data = [len(elem) for elem in body]
    lens = Series(data)
    lens_max = lens.max()
    not_max = lens[lens != lens_max]

    empty = [""]
    for ind, length in not_max.items():
        body[ind] += empty * (lens_max - length)

