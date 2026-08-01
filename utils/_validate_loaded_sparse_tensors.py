
def _validate_loaded_sparse_tensors():
    if not torch.sparse.check_sparse_tensor_invariants().is_enabled():
        # Skip sparse tensor invariants validation for better
        # performance. See check_sparse_tensor_invariants
        # documentation for how to control sparse tensor invariants
        # checking.
        _sparse_tensors_to_validate.clear()
        return
    try:
        # We disable pinning check (see check_pinning=False below) to
        # avoid gh-153143. In fact, pinning check is unnecessary
        # anywhy when loading sparse data from external sources.
        for t in _sparse_tensors_to_validate:
            if t.layout is torch.sparse_coo:
                torch._validate_sparse_coo_tensor_args(
                    t._indices(),
                    t._values(),
                    t.size(),
                    t.is_coalesced(),
                    check_pinning=False,
                )
            elif t.layout in {
                torch.sparse_csr,
                torch.sparse_csc,
                torch.sparse_bsr,
                torch.sparse_bsc,
            }:
                # TODO: Validation currently involves an expensive traversal
                # on CPU, which may include a device transfer.
                if t.layout in {torch.sparse_csr, torch.sparse_bsr}:
                    compressed_indices, plain_indices = (
                        t.crow_indices(),
                        t.col_indices(),
                    )
                else:
                    compressed_indices, plain_indices = (
                        t.ccol_indices(),
                        t.row_indices(),
                    )
                torch._validate_sparse_compressed_tensor_args(
                    compressed_indices,
                    plain_indices,
                    t.values(),
                    t.size(),
                    t.layout,
                    check_pinning=False,
                )
            else:
                raise NotImplementedError(
                    f"_validate_loaded_sparse_tensors for layout `{t.layout}`"
                )

    finally:
        _sparse_tensors_to_validate.clear()

