
def _validate_sample_input_sparse_like_fns(op_info, sample, check_validate=False):
    if (
        sample.input.layout
        in {
            torch.sparse_csr,
            torch.sparse_csc,
            torch.sparse_bsr,
            torch.sparse_bsc,
        }
        and op_info.name != "zeros_like"
    ):
        if sample.kwargs.get("layout", sample.input.layout) != sample.input.layout:
            return ErrorInput(
                sample,
                error_regex=(
                    "empty_like with different sparse layout is not supported"
                    " \\(self is Sparse(Csc|Csr|Bsc|Bsr) but you requested Sparse(Csr|Csc|Bsr|Bsc)\\)"
                ),
            )
    if sample.input.layout is torch.sparse_coo:
        return ErrorInput(
            sample,
            error_regex=(
                "Could not run 'aten::normal_' with arguments from the 'Sparse(CPU|CUDA)' backend."
            ),
        )
    if check_validate:
        _check_validate(op_info, sample)
    return sample

