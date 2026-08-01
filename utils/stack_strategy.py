
def stack_strategy(op_schema: OpSchema) -> StrategyType:
    args_schema = op_schema.args_schema
    input_tuple_strategy = args_schema[0]
    if not isinstance(input_tuple_strategy, TupleStrategy):
        raise AssertionError(f"Expected TupleStrategy, got {input_tuple_strategy}")
    input_strategies: list[OpStrategy] = []
    for child in input_tuple_strategy.children:
        if not isinstance(child, OpStrategy):
            raise AssertionError(f"Expected OpStrategy, got {child}")
        input_strategies.append(child)
    first_input_strategy = input_strategies[0]
    common_input_ndim = first_input_strategy.ndim
    dim = cast(int, args_schema[1]) if len(args_schema) > 1 else 0
    # normalize the dim to be within the output ndim (input ndim + 1),
    # since stack inserts a new dimension
    dim = normalize_dim(dim, common_input_ndim + 1)

    mesh = first_input_strategy.mesh

    follow_placements = _derive_follow_placements_from_tuple_strategy(
        op_schema.op, input_tuple_strategy
    )

    # create op strategy base on the follow placements
    op_strategy = OpStrategy([])

    input_specs = tuple(
        DTensorSpec(mesh, tuple(follow_placements))
        for _ in range(len(input_tuple_strategy.children))
    )

    # stack op would "insert" new dim, so all sharded dim >= the inserted dim need to
    # be normalized with the new Shard placement
    follow_placements = shift_shard_dims_after_insert(follow_placements, dim)
    output_spec = DTensorSpec(mesh, tuple(follow_placements))
    redistribute_cost = [
        generate_redistribute_costs(input_strategies[i], input_specs[i])
        for i in range(len(input_specs))
    ]
    op_strategy.strategies.append(
        OpSpec(
            output_specs=output_spec,
            input_specs=input_specs,
            redistribute_cost=redistribute_cost,
        )
    )
    return op_strategy

