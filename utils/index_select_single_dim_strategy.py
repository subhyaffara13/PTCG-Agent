
def index_select_single_dim_strategy(
    op: OpOverload, args_schema: ArgsType, kwargs_schema: KwargsType
) -> list[list[Placement | _ShardingPlaceholder]]:
    values_meta, dim, index_meta = args_schema
    if not isinstance(values_meta, TensorMeta):
        raise AssertionError(f"Expected TensorMeta, got {type(values_meta)}")
    if not isinstance(dim, int):
        raise AssertionError(f"Expected int, got {type(dim)}")
    dim = normalize_dim(dim, len(values_meta.shape))

    strategies: list[list[Placement | _ShardingPlaceholder]] = []

    # Shard values on any non-indexed dim (output has same ndim)
    for d in range(len(values_meta.shape)):
        if d == dim:
            continue
        strategies.append(
            [_ShardingPlaceholder(d), _ShardingPlaceholder(d), Replicate()]
        )

    # Shard index → output sharded on the indexed dim
    strategies.append([_ShardingPlaceholder(dim), Replicate(), _ShardingPlaceholder(0)])

    # Partial passthrough from values
    for reduce_op in Partial.ALL_REDUCE_OPS:
        strategies.append([Partial(reduce_op), Partial(reduce_op), Replicate()])

    return strategies

