
def index_reduce_single_dim_strategy(
    op: OpOverload, args_schema: ArgsType, kwargs_schema: KwargsType
) -> list[list[Placement | _ShardingPlaceholder]]:
    # index_reduce(self, dim, index, source, reduce) — reduces source into self at index positions.
    # No partial rules: reduce ops are "mean"/"amax"/"amin"/"prod", which don't match
    # any Partial reduce op names ("avg"/"max"/"min"/"product"/"sum").
    return _index_dim_strategy(
        args_schema,
        lambda d: [
            _ShardingPlaceholder(d),  # result
            _ShardingPlaceholder(d),  # self
            Replicate(),  # index
            _ShardingPlaceholder(d),  # source
        ],
    )

