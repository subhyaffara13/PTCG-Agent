
def _construct_standard_basis_for(
    tensors: tuple[torch.Tensor, ...], tensor_numels: tuple[int, ...]
) -> tuple[torch.Tensor, ...]:
    # This function:
    # - constructs a N=sum(tensor_numels) standard basis. i.e. an NxN identity matrix.
    # - Splits the identity matrix into chunks with each chunk size determined by `tensor_numels`.
    # - Each chunk corresponds to one tensor. The chunk has the same dtype and
    #   device as the tensor
    #
    # For example, with tensor_numels = [1, 2, 1], this function returns:
    # ( tensor([[1],     tensor([[0, 0],      tensor([[0],
    #           [0],             [1, 0],              [0],
    #           [0],             [0, 1],              [0],
    #           [0]])  ,         [0, 0]])  ,          [1]])  )
    #
    # Precondition: tensor_numels == tuple(tensor.numel() for tensor in tensors)
    # Precondition: tensors always has at least one element.
    #
    # See NOTE: [Computing jacobian with vmap and grad for multiple tensors]
    # for context behind this function. All the pre-conditions are guarded for
    # in torch.autograd.functional.jacobian.
    if len(tensors) != len(tensor_numels):
        raise AssertionError(
            f"Expected tensors and tensor_numels to have the same length, "
            f"but got {len(tensors)} and {len(tensor_numels)}"
        )
    if len(tensors) == 0:
        raise AssertionError("Expected at least one tensor")
    total_numel = sum(tensor_numels)
    chunks = tuple(
        tensor.new_zeros(total_numel, tensor_numel)
        for tensor, tensor_numel in zip(tensors, tensor_numels)
    )
    diag_start_idx = 0
    for chunk, numel in zip(chunks, tensor_numels):
        chunk.diagonal(diag_start_idx).fill_(1)
        diag_start_idx -= numel
    return chunks


def _construct_standard_basis_for(
    tensors: Sequence[torch.Tensor], tensor_numels: Sequence[int]
) -> tuple[torch.Tensor, ...] | None:
    for basis in _chunked_standard_basis_for_(tensors, tensor_numels, chunk_size=None):
        return basis
    return None

