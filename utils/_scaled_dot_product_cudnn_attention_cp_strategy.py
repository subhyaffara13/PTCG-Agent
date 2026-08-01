
def _scaled_dot_product_cudnn_attention_cp_strategy(op_schema: OpSchema) -> OpStrategy:
    """
    Strategy for cudnn attention forward with Context Parallelism support.
    """
    from torch.distributed.tensor._ops._matrix_ops import (
        _scaled_dot_product_cudnn_attention_base_strategies,
    )

    mesh = op_schema.get_mesh_from_args()
    single_mesh_dim_strategies = _scaled_dot_product_cudnn_attention_base_strategies(
        op_schema
    )

    (
        query_strategy,
        _,
        _,
        attn_bias_strategy,
        compute_log_sumexp,
        *rest_args,
    ) = op_schema.args_schema
    return_debug_mask = len(op_schema.args_schema) >= 8 and rest_args[2]
    has_attn_bias = attn_bias_strategy is not None

    # Context Parallelism: shards on the sequence dim
    logsumexp_sharding = Shard(SEQ_DIM) if compute_log_sumexp else Replicate()
    debug_attn_mask_sharding = Shard(SEQ_DIM) if return_debug_mask else None

    cp_strategy: PlacementList = [
        Shard(SEQ_DIM),  # output
        logsumexp_sharding,  # logsumexp
        None,  # cum_seq_q
        None,  # cum_seq_k
        None,  # max_q
        None,  # max_k
        None,  # philox_seed
        None,  # philox_offset
        debug_attn_mask_sharding,  # debug_attn_mask
        Shard(SEQ_DIM),  # q
        Shard(SEQ_DIM),  # k
        Shard(SEQ_DIM),  # v
    ]
    if has_attn_bias:
        cp_strategy.append(Replicate())  # attn_bias - not sharded for CP
    single_mesh_dim_strategies.append(cp_strategy)

    return expand_to_full_mesh_op_strategy(
        mesh, op_schema, single_mesh_dim_strategies, input_index=9
    )

