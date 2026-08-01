
def index_fill_scalar_single_dim_strategy(
    op: OpOverload, args_schema: ArgsType, kwargs_schema: KwargsType
) -> list[list[Placement | _ShardingPlaceholder]]:
    # index_fill(self, dim, index, value) — fills self[..., index, ...] with scalar value.
    # Partial rules: each rank fills with the same scalar v, then reduces.
    # Only idempotent reduces work: avg(v,v,...,v)=v, max(v,v,...,v)=v, min(v,v,...,v)=v.
    # sum and product fail: sum(v,v,...,v)=nv, product(v,v,...,v)=v^n.
    return _index_dim_strategy(
        args_schema,
        lambda d: [
            _ShardingPlaceholder(d),  # result
            _ShardingPlaceholder(d),  # self
            Replicate(),  # value (scalar, same on all ranks)
        ],
        [[Partial(op), Partial(op), Replicate()] for op in ("avg", "max", "min")],
    )

