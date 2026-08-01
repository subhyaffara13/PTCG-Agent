
def _make_elementwise_unary_reference(
    type_promotion_kind,
    *,
    aten_op=infer_aten_op,
    extra_meta=None,
    exact_dtype=False,
) -> Callable:
    def inner(prim: Callable):
        nonlocal aten_op

        @wraps(prim)
        @out_wrapper(exact_dtype=exact_dtype)
        @elementwise_unary_scalar_wrapper
        @elementwise_type_promotion_wrapper(
            type_promoting_args=("a",),
            type_promotion_kind=type_promotion_kind,
        )
        def _ref(a: TensorLikeType) -> TensorLikeType:
            if extra_meta is not None:
                extra_meta(a)

            output = prim(a)
            return handle_noncontiguous_outputs([a], output)

        if aten_op is infer_aten_op:
            aten_op = utils.get_aten_op(prim, prim.__name__)
        if aten_op is not None:
            register_decomposition(aten_op)(_ref)

        return _ref

    return inner

