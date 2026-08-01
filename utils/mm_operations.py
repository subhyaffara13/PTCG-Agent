
def mm_operations() -> list[AHOperation]:
    mult_dims_ops = get_mult_dims_ops()
    arith_intensity_op = AHOperation("arith_intensity", get_arith_intensity)
    return mult_dims_ops + [arith_intensity_op]

