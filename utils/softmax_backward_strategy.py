
def softmax_backward_strategy(op_schema: OpSchema) -> OpStrategy:
    grad_out_strategy, out_strategy, softmax_dim, _ = op_schema.args_schema
    grad_out_strategy = cast(OpStrategy, grad_out_strategy)
    out_strategy = cast(OpStrategy, out_strategy)
    softmax_dim = cast(int, softmax_dim)
    softmax_dim = normalize_dim(softmax_dim, grad_out_strategy.ndim)

    grad_in_strategy = OpStrategy([])
    for grad_out_placement_strat, out_placement_strat in zip(
        grad_out_strategy.strategies, out_strategy.strategies
    ):
        # follow the sharding of the grad_out or out depending on which has more shards
        grad_out_src_spec = grad_out_placement_strat.output_spec
        out_src_spec = out_placement_strat.output_spec
        src_spec = (
            grad_out_src_spec
            if grad_out_src_spec.num_shards >= out_src_spec.num_shards
            else out_src_spec
        )

        # make sure inputs are replicated along the softmax dim
        tgt_spec = DTensorSpec(
            mesh=grad_out_strategy.mesh,
            placements=replicate_reduction_dims(src_spec.placements, [softmax_dim]),
        )
        new_grad_out_spec = DTensorSpec(
            mesh=tgt_spec.mesh,
            placements=tgt_spec.placements,
            tensor_meta=grad_out_src_spec.tensor_meta,
        )
        new_out_spec = DTensorSpec(
            mesh=tgt_spec.mesh,
            placements=tgt_spec.placements,
            tensor_meta=out_src_spec.tensor_meta,
        )
        redist_grad_out_cost = generate_redistribute_costs(grad_out_strategy, tgt_spec)
        redist_out_cost = generate_redistribute_costs(out_strategy, tgt_spec)
        grad_in_strategy.strategies.append(
            OpSpec(
                output_specs=tgt_spec,
                input_specs=(new_grad_out_spec, new_out_spec),
                redistribute_cost=[redist_grad_out_cost, redist_out_cost],
            )
        )

    return grad_in_strategy

