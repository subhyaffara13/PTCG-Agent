
def _create_unary_float_meta_func(func):
    @register_meta(func)
    @out_wrapper()
    def _f(x):
        return elementwise_meta(
            x, type_promotion=ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT
        )

    return _f

