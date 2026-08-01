
def _maybe_failing_sample_inputs_sparse_reduction_sum(
    op_info, device, dtype, requires_grad, layout, **kwargs
):
    """Generator of samples that are known to fail or that were failing in past."""
    # NOTE: When fixing a failing case, remove the Exception comment
    #       but keep the `yield sample` statement.
    if layout in [
        torch.sparse_csr,
        torch.sparse_csc,
    ]:
        # NotImplementedError: Could not run 'aten::sum.IntList_out' with arguments from the 'SparseCsrCPU' backend.
        yield SampleInput(
            torch.tensor([[0, 1], [2, 3]], dtype=dtype)
            .to_sparse(layout=layout)
            .requires_grad_(requires_grad),
            kwargs=dict(dim=0, keepdim=True),
        )
        yield SampleInput(
            torch.tensor([[[0, 1]], [[2, 3]]], dtype=dtype)
            .to_sparse(layout=layout, dense_dim=1)
            .requires_grad_(requires_grad),
            kwargs=dict(dim=0),
        )
        yield SampleInput(
            torch.tensor([[0, 1], [2, 3]], dtype=dtype)
            .to_sparse(layout=layout)
            .requires_grad_(requires_grad),
            kwargs=dict(dim=(0,)),
        )
        yield SampleInput(
            torch.tensor([[0, 1], [2, 3]], dtype=dtype)
            .to_sparse(layout=layout)
            .requires_grad_(requires_grad),
            kwargs=dict(dim=(0,), keepdim=True),
        )
        yield SampleInput(
            torch.tensor([[[0, 1]], [[2, 3]]], dtype=dtype)
            .to_sparse(layout=layout, dense_dim=1)
            .requires_grad_(requires_grad),
            kwargs=dict(dim=(0,)),
        )

        # RuntimeError: torch.empty: Only batched sparse compressed (non-block) tensors are supported, but got size [2]
        yield SampleInput(
            torch.tensor([[0, 1], [2, 3]], dtype=dtype)
            .to_sparse(layout=layout)
            .requires_grad_(requires_grad),
            kwargs=dict(dim=0),
        )

    if layout in [
        torch.sparse_bsr,
        torch.sparse_bsc,
    ]:
        # RuntimeError: empty_sparse_compressed expected sparse compressed (non-block) tensor layout but got SparseBsr
        yield SampleInput(
            torch.tensor([[0, 1], [2, 3]], dtype=dtype)
            .to_sparse(layout=layout, blocksize=(2, 2))
            .requires_grad_(requires_grad),
            kwargs=dict(dim=0, keepdim=True),
        )
        yield SampleInput(
            torch.tensor([[[0, 1]], [[2, 3]]], dtype=dtype)
            .to_sparse(layout=layout, dense_dim=1, blocksize=(1, 1))
            .requires_grad_(requires_grad),
            kwargs=dict(dim=0),
        )
        yield SampleInput(
            torch.tensor([[0, 1], [2, 3]], dtype=dtype)
            .to_sparse(layout=layout, blocksize=(1, 1))
            .requires_grad_(requires_grad),
            kwargs=dict(dim=(0,)),
        )
        yield SampleInput(
            torch.tensor([[0, 1], [2, 3]], dtype=dtype)
            .to_sparse(layout=layout, blocksize=(1, 1))
            .requires_grad_(requires_grad),
            kwargs=dict(dim=(0,), keepdim=True),
        )
        yield SampleInput(
            torch.tensor([[[0, 1]], [[2, 3]]], dtype=dtype)
            .to_sparse(layout=layout, blocksize=(1, 1), dense_dim=1)
            .requires_grad_(requires_grad),
            kwargs=dict(dim=(0,)),
        )

        # RuntimeError: torch.empty: Only batched sparse compressed (non-block) tensors are supported, but got size [2]
        yield SampleInput(
            torch.tensor([[0, 1], [2, 3]], dtype=dtype)
            .to_sparse(layout=layout, blocksize=(1, 1))
            .requires_grad_(requires_grad),
            kwargs=dict(dim=0),
        )

