
def meta_rshifts(self, other):
    shift_dtype_check("rshift", self, other)
    return elementwise_meta(
        self, other, type_promotion=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT
    )

