
def gen_bvar(curr: int) -> tuple[BVar, int]:
    """
    Generate a boolean variable
    :param curr: the current counter
    :return: a boolean variable and an updated counter
    """
    curr += 1
    return BVar(curr), curr

