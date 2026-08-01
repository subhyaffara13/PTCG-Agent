
def _sparse_csr_where(mask: Tensor, input: Tensor, fill_value: Tensor) -> Tensor:
    """Sparse variant of torch.where. Supports sparse CSR tensors."""
    # TODO: implement sparse CSR specific where operator for efficiency
    return _sparse_coo_where(
        mask.to_sparse_coo(), input.to_sparse_coo(), fill_value
    ).to_sparse_csr()

