
def gen_tensor_dims(n: int, curr: int) -> tuple[list[DVar], int]:
    """
    Generate a list of tensor dimensions
    :param n:  the number of dimensions
    :param curr: the current counter
    :return: a list of dimension variables and an updated counter
    """
    dims = []
    for _ in range(n):
        dvar, curr = gen_dvar(curr)
        dims.append(dvar)
    return dims, curr

