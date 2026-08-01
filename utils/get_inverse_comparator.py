
def get_inverse_comparator(op: str) -> str:
    """Returns the inverse comparator given a comparator.

    E.g. when given "==", returns "!="

    :param str op: the comparator to look up.

    :returns: The inverse of the comparator in string format
    :raises KeyError: if input is not recognized as a comparator
    """
    return {
        "==": "!=",
        "!=": "==",
        "<": ">=",
        ">": "<=",
        "<=": ">",
        ">=": "<",
        "in": "not in",
        "not in": "in",
        "is": "is not",
        "is not": "is",
    }[op]

