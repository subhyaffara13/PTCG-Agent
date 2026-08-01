
def unsafe_split(input: Tensor, split_size: int, dim: int = 0) -> tuple[Tensor, ...]:
    return aten.split.Tensor(input, split_size, dim)


def unsafe_split(
    g: jit_utils.GraphContext, self, split_size_or_sizes, dim, _outputs=None
):
    return split(g, self, split_size_or_sizes, dim, _outputs)


def unsafe_split(
    g: jit_utils.GraphContext, self, split_size_or_sizes, dim, _outputs=None
):
    return split(g, self, split_size_or_sizes, dim, _outputs)

