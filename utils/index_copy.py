
def index_copy(x: TensorLike, dim: int, index: TensorLike, tensor: TensorLike):
    return _index_copy(x, dim, index, tensor, inplace=False)


def index_copy(x: TensorLike, dim: int, index: TensorLike, tensor: TensorLike):
    return x.clone(memory_format=torch.contiguous_format).index_copy_(
        dim, index, tensor
    )


def index_copy(g: jit_utils.GraphContext, self, dim, index, source):
    _expanded_index_shape, expanded_index = symbolic_helper._index_fill_reshape_helper(
        g, self, dim, index
    )
    return scatter(g, self, dim, expanded_index, source)


def index_copy(g: jit_utils.GraphContext, self, dim, index, source):
    _expanded_index_shape, expanded_index = symbolic_helper._index_fill_reshape_helper(
        g, self, dim, index
    )
    return scatter(g, self, dim, expanded_index, source)

