
def meta__add_relu(self, other, alpha=1) -> Tensor:
    return elementwise_meta(
        self, other, type_promotion=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT
    )

