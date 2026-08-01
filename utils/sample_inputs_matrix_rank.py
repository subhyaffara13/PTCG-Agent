
def sample_inputs_matrix_rank(op_info, device, dtype, requires_grad=False, **kwargs):
    """
    This function produces inputs for matrix rank that test
    all possible combinations for atol and rtol
    """

    def make_tol_arg(kwarg_type, inp):
        if kwarg_type == "none":
            return None
        if kwarg_type == "float":
            return 1.0
        if kwarg_type != "tensor":
            raise AssertionError(f"Expected kwarg_type == 'tensor', got {kwarg_type!r}")
        return torch.ones(inp.shape[:-2], device=device)

    for tol_type in ["float", "tensor"]:
        for atol_type, rtol_type in product(["none", tol_type], repeat=2):
            if (
                not atol_type and not rtol_type
            ):  # default behavior, so skipped here so it's not tested 2 extra times
                continue
            for sample in sample_inputs_linalg_invertible(
                op_info, device, dtype, requires_grad
            ):
                if sample.kwargs != {}:
                    raise AssertionError(
                        f"Expected sample.kwargs == {{}}, got {sample.kwargs}"
                    )
                sample.kwargs = {
                    "atol": make_tol_arg(atol_type, sample.input),
                    "rtol": make_tol_arg(rtol_type, sample.input),
                }
                yield sample

    # default kwargs
    yield from sample_inputs_linalg_invertible(op_info, device, dtype, requires_grad)

