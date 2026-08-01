
def _mm_like_strategy(
    mm_equation: str, mesh: DeviceMesh, op_schema: OpSchema
) -> OpStrategy:
    self_strategy, mat2_strategy = op_schema.args_schema
    if not isinstance(self_strategy, OpStrategy):
        raise AssertionError(f"Expected OpStrategy, got {type(self_strategy)}")
    if not isinstance(mat2_strategy, OpStrategy):
        raise AssertionError(f"Expected OpStrategy, got {type(mat2_strategy)}")
    # generate all possible strategies for mm
    mm_strategy = gen_einsum_strategies(mm_equation, mesh)
    # filter out invalid strategies and associate costs
    strategies = mm_strategy.strategies
    filtered_strategies = []
    for strtg in strategies:
        if strtg.input_specs is None:
            raise AssertionError(
                f"Expected input_specs to be not None, got {strtg.input_specs}"
            )
        self_spec = strtg.input_specs[0]
        mat2_spec = strtg.input_specs[1]
        if is_tensor_shardable(
            self_strategy.shape, self_spec, allow_unbacked_sharding=True
        ) and is_tensor_shardable(
            mat2_strategy.shape, mat2_spec, allow_unbacked_sharding=True
        ):
            redistribute_cost = [
                generate_redistribute_costs(self_strategy, self_spec),
                generate_redistribute_costs(mat2_strategy, mat2_spec),
            ]
            strtg.redistribute_cost = redistribute_cost
            filtered_strategies.append(strtg)

    mm_strategy.strategies = filtered_strategies

    return mm_strategy

