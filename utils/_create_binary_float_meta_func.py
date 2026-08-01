
def _create_binary_float_meta_func(func):
    @register_meta(func)
    @out_wrapper()
    def _f(x, y):
        return elementwise_meta(
            x, y, type_promotion=ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT
        )

    return _f

