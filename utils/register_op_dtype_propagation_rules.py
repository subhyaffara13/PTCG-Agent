
def register_op_dtype_propagation_rules(
    name: str,
    type_promotion_kind: ELEMENTWISE_TYPE_PROMOTION_KIND,
    override_return_dtype: torch.dtype | None,
) -> None:
    op_dtype_propagation_rules[name] = OpDtypeRule(
        type_promotion_kind, override_return_dtype
    )

