
def meta_complex(real, imag):
    if not real.dtype.is_floating_point:
        raise AssertionError(f"real must be floating point, got {real.dtype}")
    if not imag.dtype.is_floating_point:
        raise AssertionError(f"imag must be floating point, got {imag.dtype}")
    result = elementwise_meta(
        real.to(corresponding_complex_dtype(real.dtype)),
        imag.to(corresponding_complex_dtype(imag.dtype)),
        type_promotion=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
    )
    return result

