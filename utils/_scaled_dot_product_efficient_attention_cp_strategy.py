
def _scaled_dot_product_efficient_attention_cp_strategy(
    op_schema: OpSchema,
) -> OpStrategy:
    """
    Strategy for efficient attention forward with Context Parallelism support.
    """
    from torch.distributed.tensor._ops._matrix_ops import (
        _scaled_dot_product_efficient_attention_base_strategies,
    )

    mesh = op_schema.get_mesh_from_args()
    single_mesh_dim_strategies = (
        _scaled_dot_product_efficient_attention_base_strategies(op_schema)
    )

    # Add Context Parallelism strategy
    has_attn_bias = op_schema.args_schema[3] is not None

    cp_strategy: PlacementList = [
        Shard(SEQ_DIM),  # output
        Shard(SEQ_DIM),  # logsumexp
        None,  # philox_seed
        None,  # philox_offset
        Shard(SEQ_DIM),  # q
        Shard(SEQ_DIM),  # k
        Shard(SEQ_DIM),  # v
    ]
    if has_attn_bias:
        cp_strategy.append(Replicate())  # attn bias - not sharded for CP
    single_mesh_dim_strategies.append(cp_strategy)

    return expand_to_full_mesh_op_strategy(
        mesh, op_schema, single_mesh_dim_strategies, input_index=4
    )

