
def _pad_chunk(
    tensors: list[Tensor],
    dim: int,
    num_chunks: int,
) -> list[Tensor]:
    padded_tensors = []
    for tensor in tensors:
        tensor_size = tensor.size()
        pad_along_dim = (tensor_size[dim] + num_chunks - 1) // num_chunks * num_chunks
        if pad_along_dim != tensor_size[dim]:
            # Use aten.constant_pad_nd instead of copy_ for functionalization
            pad = [0] * 2 * (tensor.ndim - dim - 1) + [
                0,
                pad_along_dim - tensor_size[dim],
            ]
            tensor = aten.constant_pad_nd(tensor, pad, 0)
        view_size = tensor_size[:dim] + torch.Size([num_chunks, -1])
        padded_tensors.append(tensor.reshape(view_size))
    return padded_tensors

