
def addmm_single_dim_strategy(
    op: OpOverload, args_schema: ArgsType, kwargs_schema: KwargsType
) -> list[list[Placement | _ShardingPlaceholder]]:
    bias_meta = args_schema[0]
    if not isinstance(bias_meta, TensorMeta):
        raise AssertionError
    return gen_single_dim_einsum_strategies("mk,kn->mn", bias_shape=bias_meta.shape)

