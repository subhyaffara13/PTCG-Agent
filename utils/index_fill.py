
def index_fill(
    x: TensorLike, dim: int, index: TensorLike, value: NumberType | TensorLike
):
    return _index_fill(x, dim, index, value, inplace=False)


def index_fill(g: jit_utils.GraphContext, self, dim, index, value):
    expanded_index_shape, expanded_index = symbolic_helper._index_fill_reshape_helper(
        g, self, dim, index
    )
    value = symbolic_helper._maybe_get_scalar(value)
    value = symbolic_helper._if_scalar_type_as(value, self)
    expanded_value = opset9.expand(g, value, expanded_index_shape, None)
    return scatter(g, self, dim, expanded_index, expanded_value)


def index_fill(g: jit_utils.GraphContext, self, dim, index, value):
    expanded_index_shape, expanded_index = symbolic_helper._index_fill_reshape_helper(
        g, self, dim, index
    )
    value = symbolic_helper._maybe_get_scalar(value)
    value = symbolic_helper._if_scalar_type_as(value, self)
    expanded_value = expand(g, value, expanded_index_shape, None)

    return scatter(g, self, dim, expanded_index, expanded_value)

