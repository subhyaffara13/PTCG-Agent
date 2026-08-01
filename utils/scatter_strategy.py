
def scatter_strategy(op_schema: OpSchema) -> StrategyType:
    mesh = op_schema.get_mesh_from_args()
    single_mesh_dim_strategies = []

    # placement list stores placements of [output, input, index, src]
    # first we always have replicate all for inputs and output
    if len(op_schema.args_strategy) < 3:
        # scatter_.src/scatter.src with src be float number instead of tensor
        all_replicate: PlacementList = [Replicate()] * 3
    else:
        all_replicate = [Replicate()] * 4
    single_mesh_dim_strategies.append(all_replicate)

    # TODO: see if we can support input sharding pattern
    op_strategy = expand_to_full_mesh_op_strategy(
        mesh,
        op_schema,
        single_mesh_dim_strategies,
        inplace_op=op_schema.is_inplace_op(),
    )
    return op_strategy

