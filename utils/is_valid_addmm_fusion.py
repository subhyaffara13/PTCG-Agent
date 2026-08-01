
def is_valid_addmm_fusion(match):
    mat1, mat2 = match.args
    inp = match.kwargs["inp"]

    if not (
        isinstance(inp, torch.fx.Node) and isinstance(inp.meta["val"], torch.Tensor)
    ):
        return False  # Input is a number

    in_shape = inp.meta["val"].shape
    mm_shape = mat1.meta["val"].shape[0], mat2.meta["val"].shape[1]
    matched = is_expandable_to(in_shape, mm_shape)
    if not matched:
        return False  # Shape mismatch

    inp_dtype = inp.meta["val"].dtype

    # aten cublas integration assumes equal dtypes
    if inp_dtype != mat1.meta["val"].dtype or inp_dtype != mat2.meta["val"].dtype:
        return False

    return not should_prefer_unfused_addmm(match)

