
def semi_sparse_values(func, types, args=(), kwargs=None) -> torch.Tensor:
    if len(args) != 1:
        raise AssertionError(f"expected 1 arg, got {len(args)}")
    A = args[0]
    if not isinstance(A, torch.sparse.SparseSemiStructuredTensor):
        raise AssertionError(
            f"expected SparseSemiStructuredTensor, got {type(A).__name__}"
        )
    if A.packed is None:
        raise AssertionError("A.packed must not be None")
    if A.meta is None:
        m, k = A.shape
        num_kept_elements = m * k // 2
        return A.packed.ravel()[:num_kept_elements:].view(m, -1)
    else:
        return A.packed.detach()

