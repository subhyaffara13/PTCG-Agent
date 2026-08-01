
def check_dim_size(tensor, dim, dim_size, size):
    torch._check(
        tensor.dim() == dim and tensor.shape[dim_size] == size,
        lambda: f"Expected a tensor of dimension {dim} and tensor.size[{dim_size}] == {size}, "
        + f"but got : dimension {tensor.dim()} and tensor.size[{dim_size}] = {tensor.shape[dim_size]}",
    )

