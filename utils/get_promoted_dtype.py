
def get_promoted_dtype(
    *args: Sequence[tuple[torch.dtype, bool]],
    type_promotion_kind: ELEMENTWISE_TYPE_PROMOTION_KIND | None = None,
):
    def construct_input(inp):
        if inp[1]:
            return torch.empty([], dtype=inp[0])
        else:
            return torch.empty([1], dtype=inp[0])

    inps = [construct_input(arg) for arg in args]
    _, dtype = torch._prims_common.elementwise_dtypes(
        *inps,
        type_promotion_kind=(
            type_promotion_kind
            if type_promotion_kind
            else ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT
        ),
    )
    return dtype


def get_promoted_dtype(
    *args: Any,
    type_promotion_kind: ELEMENTWISE_TYPE_PROMOTION_KIND,
    return_compute_dtype: bool = False,
) -> torch.dtype:
    def construct_input(inp: Any) -> Any:
        if isinstance(inp, (Number, sympy.Basic)):
            return inp
        else:
            dim = len(inp.get_size())
            # construct a tmp tensor to feed into torch.result_type
            return torch.zeros([1] * dim, dtype=inp.get_dtype())

    inps = [construct_input(arg) for arg in args]
    compute_dtype, result_dtype = elementwise_dtypes(
        *inps, type_promotion_kind=type_promotion_kind
    )
    return compute_dtype if return_compute_dtype else result_dtype

