
def index_fill_tensor_single_dim_strategy(
    op: OpOverload, args_schema: ArgsType, kwargs_schema: KwargsType
) -> list[list[Placement | _ShardingPlaceholder]]:
    # index_fill(self, dim, index, value) — fills self[..., index, ...] with 0-d tensor value.
    # Partial rules: each rank fills with its partial value v_i, then reduces.
    # All reduce ops work because reduce(v_0, ..., v_{n-1}) = V (the global value)
    # regardless of op, since fill is a pure replacement (no mixing with self).
    return _index_dim_strategy(
        args_schema,
        lambda d: [
            _ShardingPlaceholder(d),  # result
            _ShardingPlaceholder(d),  # self
            Replicate(),  # index
            Replicate(),  # value
        ],
        [
            [Partial(op), Partial(op), Replicate(), Partial(op)]
            for op in Partial.ALL_REDUCE_OPS
        ],
    )

