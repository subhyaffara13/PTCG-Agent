
def _cat_np(input_seq, dim=0):
    inputs = tuple(a for a in input_seq if not (a.ndim == 1 and a.size == 0))

    if len(inputs) == 0:
        np_dtype = _elementwise_type_promo_np(
            input_seq,
            type_promotion_kind=prims.utils.ELEMENTWISE_TYPE_PROMOTION_KIND.NO_OPMATH)
        return np.empty(0, dtype=np_dtype)

    return np.concatenate(inputs, axis=dim)

