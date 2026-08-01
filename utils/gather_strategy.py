
def gather_strategy(op_schema: OpSchema) -> StrategyType:
    mesh = op_schema.get_mesh_from_args()
    input_strategy = cast(OpStrategy, op_schema.args_schema[0])
    dim = cast(int, op_schema.args_schema[1])
    dim = normalize_dim(dim, input_strategy.ndim)
    index_strategy = cast(OpStrategy, op_schema.args_schema[2])

    input_shape = input_strategy.shape
    index_shape = index_strategy.shape

    single_mesh_dim_strategies = []

    # placement list stores placements of [output, input, index]
    # first we always have replicate all for inputs and output
    all_replicate: PlacementList = [Replicate()] * 3
    single_mesh_dim_strategies.append(all_replicate)

    # input sharding, input sharded, index accepts mask partial, output follows index
    # this only works when the input is sharded on the gather dimension, and
    # index has size 1 on the gather dimension
    if dim < len(index_shape) and index_shape[dim] == 1:
        index_partial_placement = _MaskPartial(offset_shape=input_shape, offset_dim=dim)
        input_sharding: PlacementList = [
            index_partial_placement,
            Shard(dim),
            index_partial_placement,
        ]
        single_mesh_dim_strategies.append(input_sharding)

    # index sharding, input replicated, index sharded, output follows index
    # this only works when the sharding dimension is the gather dimension
    index_sharding: PlacementList = [Shard(dim), Replicate(), Shard(dim)]
    single_mesh_dim_strategies.append(index_sharding)

    if len(input_shape) == len(index_shape):
        for d in range(len(input_shape)):
            if d != dim:
                sharding: PlacementList = [Shard(d), Shard(d), Shard(d)]
                single_mesh_dim_strategies.append(sharding)

    return expand_to_full_mesh_op_strategy(
        mesh, op_schema, single_mesh_dim_strategies, input_index=1
    )

