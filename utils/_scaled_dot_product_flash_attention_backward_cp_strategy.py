
def _scaled_dot_product_flash_attention_backward_cp_strategy(
    op_schema: OpSchema,
) -> OpStrategy:
    """
    Strategy for flash attention backward with Context Parallelism support.
    """
    from torch.distributed.tensor._ops._matrix_ops import (
        _scaled_dot_product_flash_attention_backward_base_strategies,
    )

    mesh = op_schema.get_mesh_from_args(validate=False)
    single_mesh_dim_strategies = (
        _scaled_dot_product_flash_attention_backward_base_strategies(op_schema)
    )

    tensor_input_indices = [
        i
        for i, arg_spec in enumerate(op_schema.args_schema)
        if isinstance(arg_spec, OpStrategy)
    ]
    num_tensor_inputs = len(tensor_input_indices)

    # Context Parallelism: shards on the sequence dim
    cp_strategy: PlacementList = [
        Shard(SEQ_DIM),  # grad_q
        Shard(SEQ_DIM),  # grad_k
        Shard(SEQ_DIM),  # grad_v
        Shard(SEQ_DIM),  # grad_output
        Shard(SEQ_DIM),  # q
        Shard(SEQ_DIM),  # k
        Shard(SEQ_DIM),  # v
        Shard(SEQ_DIM),  # output
        Shard(SEQ_DIM),  # logsumexp
    ]
    cp_strategy.extend([Replicate()] * (num_tensor_inputs - 6))
    single_mesh_dim_strategies.append(cp_strategy)

    return expand_to_full_mesh_op_strategy(
        mesh, op_schema, single_mesh_dim_strategies, input_index=3
    )

