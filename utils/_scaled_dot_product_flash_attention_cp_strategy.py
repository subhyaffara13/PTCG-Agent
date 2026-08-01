
def _scaled_dot_product_flash_attention_cp_strategy(op_schema: OpSchema) -> OpStrategy:
    """
    Strategy for flash attention forward with Context Parallelism support.
    This includes the base strategies plus CP-specific sequence dimension sharding.
    """
    # Import here to avoid circular dependency
    from torch.distributed.tensor._ops._matrix_ops import (
        _scaled_dot_product_flash_attention_base_strategies,
    )

    # Get the base strategies (without CP modifications)
    mesh = op_schema.get_mesh_from_args()
    single_mesh_dim_strategies = _scaled_dot_product_flash_attention_base_strategies(
        op_schema
    )

    # Add Context Parallelism strategy: shards on the sequence dim
    return_debug_mask = len(op_schema.args_schema) >= 6 and op_schema.args_schema[5]
    debug_attn_mask_sharding = Shard(SEQ_DIM) if return_debug_mask else Replicate()

    cp_strategy: PlacementList = [
        Shard(SEQ_DIM),  # output
        Shard(SEQ_DIM),  # logsumexp
        None,  # cum_seq_q
        None,  # cum_seq_k
        None,  # max_q
        None,  # max_k
        Replicate(),  # rng_state
        None,  # unused
        debug_attn_mask_sharding,  # debugattn
        Shard(SEQ_DIM),  # q
        Shard(SEQ_DIM),  # k
        Shard(SEQ_DIM),  # v
    ]
    single_mesh_dim_strategies.append(cp_strategy)

    return expand_to_full_mesh_op_strategy(
        mesh, op_schema, single_mesh_dim_strategies, input_index=9
    )

