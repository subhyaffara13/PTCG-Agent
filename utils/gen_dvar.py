
def gen_dvar(curr: int) -> tuple[DVar, int]:
    """
    Generate a dimension variable
    :param curr: the current counter
    :return: a dimension variable and an updated counter
    """
    curr += 1
    return DVar(curr), curr

