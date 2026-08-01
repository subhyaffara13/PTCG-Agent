
def dict___eq__(d: dict[T, U], other: dict[T, U]) -> bool:
    if (len(d) != len(other)) or (d.keys() != other.keys()):
        return False

    if all(isinstance(a, OrderedDict) for a in (d, other)):
        return list(d.items()) == list(other.items())

    for k, v in d.items():
        if v != other[k]:
            return False

    return True

