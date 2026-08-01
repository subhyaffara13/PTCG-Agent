
def meta_polygamma(n: int, self: Tensor) -> Tensor:
    torch._check(n >= 0, lambda: "polygamma(n, x) does not support negative n.")
    _, result_dtype = elementwise_dtypes(
        self,
        type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT,
    )
    return torch.empty_like(self, dtype=result_dtype)

