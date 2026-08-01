
def space_indentation(s: str) -> int:
    """The number of leading spaces in a string.

    :param str s: input string

    :rtype: int
    :return: number of leading spaces
    """
    return len(s) - len(s.lstrip(" "))

