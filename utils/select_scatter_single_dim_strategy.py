
def select_scatter_single_dim_strategy(
    op: OpOverload,
    args_schema: ArgsType,
    kwargs_schema: KwargsType,
) -> list[list[Placement | _ShardingPlaceholder]]:
    input_meta = args_schema[0]
    if not isinstance(input_meta, TensorMeta):
        raise AssertionError(f"Expected TensorMeta, got {type(input_meta)}")
    ndim = len(input_meta.shape)
    dim = normalize_dim(cast(int, args_schema[2]), ndim)
    # [output, self, src] — src has the select dim removed
    strategies: list[list[Placement | _ShardingPlaceholder]] = []
    for d in range(ndim):
        if d == dim:
            continue
        strategies.append(
            [
                _ShardingPlaceholder(d),
                _ShardingPlaceholder(d),
                _ShardingPlaceholder(d if d < dim else d - 1),
            ]
        )
    return strategies

