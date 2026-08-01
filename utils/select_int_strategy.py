
def select_int_strategy(op_schema: OpSchema) -> StrategyType:
    """
    In this select op, first determine the input specs, then determine the output specs.
    - Input specs:
        - If the input is sharded on the selected dim, unshard it and change to replicate.
        - Otherwise, keep the original input specs.
    - Output specs:
        - It checks the input specs with the following cases:
        - Case 1 shard_dim == selected_dim: not possible as the input is already unsharded.
        - Case 2 shard_dim < selected_dim: keep the input specs.
        - Case 3 shard_dim > selected_dim: shard_dim -= 1.
    """
    input_strategy = op_schema.args_schema[0]
    if not isinstance(input_strategy, OpStrategy):
        raise AssertionError(f"Expected OpStrategy, got {type(input_strategy)}")
    if len(op_schema.args_schema) != 3:
        raise AssertionError(f"Expected 3 args, got {len(op_schema.args_schema)}")
    selected_dim, index = (
        cast(int, op_schema.args_schema[1]),
        cast(int, op_schema.args_schema[2]),
    )
    input_shape = input_strategy.shape
    input_ndim = input_strategy.ndim
    selected_dim = normalize_dim(selected_dim, input_ndim)
    index = normalize_dim(index, input_shape[selected_dim])

    select_strategy = OpStrategy([])
    for arg_strategy in input_strategy.strategies:
        arg_spec = arg_strategy.output_spec

        # determine input spec
        input_specs = arg_spec
        if is_tensor_dim_sharded(arg_spec, dim=selected_dim):
            # if input is sharded on the selected dim, need to unshard it, change to replicate
            arg_target_placements = unshard_tensor_dim(
                arg_spec.placements, dim=selected_dim
            )
            input_specs = DTensorSpec(arg_spec.mesh, arg_target_placements)  # R

        # determine output spec
        output_specs = input_specs
        if input_specs.is_sharded():
            # handle cases with sharded_dim != selected_dim
            output_placements = shift_shard_dims_after_remove(
                input_specs.placements, selected_dim
            )
            output_specs = DTensorSpec(
                arg_spec.mesh, placements=tuple(output_placements)
            )

        select_strategy.strategies.append(
            OpSpec(
                output_specs=output_specs,
                input_specs=(input_specs,),
            )
        )
    return select_strategy

