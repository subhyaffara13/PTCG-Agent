
def _to_copy_single_dim_strategy(
    op: OpOverload, args_schema: ArgsType, kwargs_schema: KwargsType
) -> list[list[Placement | _ShardingPlaceholder]]:
    input_meta = cast(TensorMeta, args_schema[0])
    src_dtype = input_meta.dtype
    target_dtype = cast(torch.dtype | None, kwargs_schema.get("dtype", None))

    strategies: list[list[Placement | _ShardingPlaceholder]] = []
    for dim in range(len(input_meta.shape)):
        strategies.append([_ShardingPlaceholder(dim), _ShardingPlaceholder(dim)])
    for reduce_op in Partial.ALL_REDUCE_OPS:
        if not _partial_needs_reduce_for_dtype_cast(reduce_op, src_dtype, target_dtype):
            strategies.append([Partial(reduce_op), Partial(reduce_op)])
    return strategies

