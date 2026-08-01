
def dist(input: Tensor, other: Tensor, p: float = 2):
    return aten.norm(input - other, p=p)

