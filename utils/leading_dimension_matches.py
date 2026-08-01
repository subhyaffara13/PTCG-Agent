
def leading_dimension_matches(tensors: list[Tensor], dim: int):
    leading_dim_sizes = tensors[0].size()[:dim]
    for tensor in tensors:
        torch._check(
            tensor.size()[:dim] == leading_dim_sizes,
            lambda: "_chunk_cat expects same sizes of 0,...,dim-1 dimensions for all tensors",
        )

