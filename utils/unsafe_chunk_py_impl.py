
def unsafe_chunk_py_impl(tensor, chunks, dim=0) -> list[Tensor]:
    dim_size = tensor.size(dim)
    split_size = (dim_size + chunks - 1) // chunks

    if split_size == 0 and dim_size == 0:
        split_sizes = [split_size for _ in range(chunks)]
        split_sizes[chunks - 1] = split_size - (split_size * chunks - dim_size)
        return torch.ops.aten.unsafe_split_with_sizes.default(tensor, split_sizes, dim)
    return torch.ops.aten.unsafe_split.Tensor(tensor, split_size, dim)

