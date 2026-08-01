
def meta_round(self, **kwargs):
    return elementwise_meta(
        self, type_promotion=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT
    )

