
def index_fill_(
    x: TensorLike, dim: int, index: TensorLike, value: NumberType | TensorLike
):
    return _index_fill(x, dim, index, value, inplace=True)

