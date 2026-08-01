
def _linalg_solve_ex(
    A: Tensor,
    B: Tensor,
    *,
    left: bool = True,
    check_errors: bool = False,
    result: Tensor | None = None,
    LU: Tensor | None = None,
    pivots: Tensor | None = None,
    info: Tensor | None = None,
) -> tuple[Tensor, Tensor, Tensor, Tensor]:
    checkFloatingOrComplex(A, "linalg.solve")
    torch._check(
        A.dtype == B.dtype,
        lambda: (
            f"linalg.solve: Expected A and B to have the same dtype, but found A of type "
            f"{A.dtype} and B of type {B.dtype} instead"
        ),
    )
    vector_case = linalg_solve_is_vector_rhs(A, B)
    B_ = B.unsqueeze(-1) if vector_case else B
    checkInputsSolver(A, B_, left, "linalg.solve")
    B_broad_shape, _ = _linalg_broadcast_batch_dims(B_, A)
    torch._check(
        left or not vector_case,
        lambda: (
            "linalg.solve: Vector broadcasting of the left hand side is not supported for left=False. "
            "In this case linalg.solve is equivalent to B / A.squeeze(-1)"
        ),
    )
    result_shape = B_broad_shape[:-1] if vector_case else B_broad_shape
    result_ = torch.empty_strided(
        size=result_shape,
        stride=make_contiguous_strides_for(result_shape, not left),
        dtype=B.dtype,
        device=B.device,
    )
    shape = A.shape
    LU_ = torch.empty_strided(
        size=shape,
        stride=make_contiguous_strides_for(shape, False),
        dtype=A.dtype,
        device=A.device,
    )
    pivots_ = A.new_empty(shape[:-1], dtype=torch.int32)
    info_ = A.new_empty(shape[:-2], dtype=torch.int32)
    out = (result, LU, pivots, info)
    res = (result_, LU_, pivots_, info_)
    if all(x is not None for x in out):
        for r, o in zip(res, out):
            # resize and copy operations are done in-place
            _maybe_resize_out(o, r.shape)  # type: ignore[arg-type]
            # strides are not copied in out_wrapper
            o.as_strided_(r.shape, r.stride())  # type: ignore[union-attr]
            _safe_copy_out(copy_from=r, copy_to=o, exact_dtype=False)  # type: ignore[arg-type]
    return res

