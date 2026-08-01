
def _lu_with_infos(A, pivot=True, get_infos=False, out=None):
    # type: (Tensor, bool, bool, Optional[tuple[Tensor, Tensor, Tensor]]) -> tuple[Tensor, Tensor, Tensor]
    if has_torch_function_unary(A):
        return handle_torch_function(
            lu, (A,), A, pivot=pivot, get_infos=get_infos, out=out
        )
    result = _lu_impl(A, pivot, get_infos, out)
    if out is not None:
        _check_list_size(len(out), get_infos, out)
        for i in range(len(out)):
            out[i].resize_as_(result[i]).copy_(result[i])
        return out
    else:
        return result  # A_LU, pivots, infos

