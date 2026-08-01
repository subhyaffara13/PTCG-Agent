
def unsafe_split_with_sizes(
    input: Tensor, split_sizes: list[int], dim: int = 0
) -> tuple[Tensor, ...]:
    return aten.split_with_sizes.default(input, split_sizes, dim)


def unsafe_split_with_sizes(
    g: jit_utils.GraphContext, self, split_sizes, dim, _outputs=None
):
    return split_with_sizes(g, self, split_sizes, dim, _outputs)


def unsafe_split_with_sizes(
    g: jit_utils.GraphContext, self, split_sizes, dim, _outputs=None
):
    return split_with_sizes(g, self, split_sizes, dim, _outputs)

