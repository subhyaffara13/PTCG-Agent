
def addmm_impl(
    input: ComplexTensor,
    mat1: ComplexTensor,
    mat2: ComplexTensor,
    out_dtype: torch.dtype | None = None,
    beta: int | float | complex = 1,
    alpha: int | float | complex = 1,
) -> ComplexTensor:
    ret = beta * input + alpha * torch.mm(mat1, mat2)
    if not isinstance(ret, ComplexTensor):
        raise AssertionError(f"ret must be a ComplexTensor, got {type(ret)}")
    ret_r, ret_i = split_complex_tensor(ret)
    if out_dtype is not None:
        out_dtype = COMPLEX_TO_REAL[out_dtype]
        ret_r, ret_i = ret_r.to(out_dtype), ret_i.to(out_dtype)
    return ComplexTensor(ret_r, ret_i)

