
def bucketize_single_dim_strategy(
    op: OpOverload, args_schema: ArgsType, kwargs_schema: KwargsType
) -> list[list[Placement | _ShardingPlaceholder]]:
    """Bucketize returns indices into a sorted boundary tensor.

    Three families of strategies:
    1. Shard the input (and output) on any dim, keep boundaries replicated.
    2. Shard boundaries on dim 0, replicate input, output is Partial("sum").
       Each rank counts how many of its local boundary values each input
       element exceeds; summing across ranks gives the correct global index.
    3. Partial("max") or Partial("min") input with replicated boundaries.
       Bucketize is monotonically non-decreasing in its input, so reducing
       local bucket indices with max (or min) across ranks gives the same
       result as bucketizing the reduced input values.
    """
    input_meta, _boundaries_meta = args_schema
    if not isinstance(input_meta, TensorMeta):
        raise AssertionError(f"Expected TensorMeta, got {type(input_meta)}")
    strategies: list[list[Placement | _ShardingPlaceholder]] = []
    for dim in range(len(input_meta.shape)):
        strategies.append(
            [_ShardingPlaceholder(dim), _ShardingPlaceholder(dim), Replicate()]
        )
    strategies.append([Partial("sum"), Replicate(), _ShardingPlaceholder(0)])
    for reduce_op in ("max", "min"):
        strategies.append([Partial(reduce_op), Partial(reduce_op), Replicate()])
    return strategies

