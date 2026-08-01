
def elementwise_meta(
    *args,
    type_promotion: ELEMENTWISE_TYPE_PROMOTION_KIND,
):
    # Perform type promotion, as this is expected from prim_metafunction
    _, result_dtype = utils.elementwise_dtypes(
        *args,
        type_promotion_kind=type_promotion,
    )
    args = [_maybe_convert_to_dtype(x, result_dtype) for x in args]

    # Broadcast
    args = _maybe_broadcast(*args)

    # Perform prim checks
    return _prim_elementwise_meta(
        *args, type_promotion=ELEMENTWISE_PRIM_TYPE_PROMOTION_KIND.DEFAULT
    )

