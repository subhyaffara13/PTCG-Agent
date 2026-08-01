
def _floor_divide_np(a, b):
    dtype = _elementwise_type_promo_np(
        a,
        b,
        type_promotion_kind=prims.utils.ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT)
    if isinstance(a, np.ndarray):
        a = a.astype(dtype)
    if isinstance(b, np.ndarray):
        b = b.astype(dtype)
    return np.floor_divide(a, b)

