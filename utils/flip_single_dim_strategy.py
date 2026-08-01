
def flip_single_dim_strategy(
    op: OpOverload, args_schema: ArgsType, kwargs_schema: KwargsType
) -> list[list[Placement | _ShardingPlaceholder]]:
    input_meta = args_schema[0]
    if not isinstance(input_meta, TensorMeta):
        raise AssertionError(f"Expected TensorMeta, got {type(input_meta)}")
    ndim = len(input_meta.shape)
    raw_dims = cast(list[int], args_schema[1])
    active_dims = {normalize_dim(d, ndim) for d in raw_dims}
    return _shard_inactive_dims(ndim, active_dims) + _pass_through_partials()

