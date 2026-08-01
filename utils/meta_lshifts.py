
def meta_lshifts(self, other):
    shift_dtype_check("lshift", self, other)
    return elementwise_meta(
        self, other, type_promotion=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT
    )

