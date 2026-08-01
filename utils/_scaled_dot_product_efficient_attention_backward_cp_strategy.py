
def _scaled_dot_product_efficient_attention_backward_cp_strategy(
    op_schema: OpSchema,
) -> OpStrategy:
    """
    Strategy for efficient attention backward with Context Parallelism support.
    """
    from torch.distributed.tensor._ops._matrix_ops import (
        _scaled_dot_product_efficient_attention_backward_base_strategies,
    )

    mesh = op_schema.get_mesh_from_args(validate=False)
    single_mesh_dim_strategies = (
        _scaled_dot_product_efficient_attention_backward_base_strategies(op_schema)
    )

    has_attn_bias = op_schema.args_schema[4] is not None

    # Context Parallelism: shards on the sequence dim
    cp_strategy: PlacementList = [
        Shard(SEQ_DIM),  # grad_q
        Shard(SEQ_DIM),  # grad_k
        Shard(SEQ_DIM),  # grad_v
        Shard(1) if has_attn_bias else None,  # grad_bias
        Shard(SEQ_DIM),  # grad_output
        Shard(SEQ_DIM),  # q
        Shard(SEQ_DIM),  # k
        Shard(SEQ_DIM),  # v
        Shard(SEQ_DIM),  # output
        Shard(SEQ_DIM),  # logsumexp
    ]
    if has_attn_bias:
        cp_strategy.insert(8, Shard(1))  # attn_bias input
    cp_strategy.extend([Replicate(), Replicate()])
    single_mesh_dim_strategies.append(cp_strategy)

    return expand_to_full_mesh_op_strategy(
        mesh, op_schema, single_mesh_dim_strategies, input_index=4
    )

