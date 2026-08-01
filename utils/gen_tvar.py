
def gen_tvar(curr: int) -> tuple[TVar, int]:
    """
    Generate a tensor variable
    :param curr: The current counter
    :return: a tensor variable and the updated counter
    """
    curr += 1
    return TVar(curr), curr

