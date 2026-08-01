
def bmm_single_dim_strategy(
    op: OpOverload, args_schema: ArgsType, kwargs_schema: KwargsType
) -> list[list[Placement | _ShardingPlaceholder]]:
    return gen_single_dim_einsum_strategies("bmk,bkn->bmn")

