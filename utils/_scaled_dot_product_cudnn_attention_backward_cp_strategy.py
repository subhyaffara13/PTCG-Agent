
def _scaled_dot_product_cudnn_attention_backward_cp_strategy(
    op_schema: OpSchema,
) -> OpStrategy:
    """
    Strategy for cudnn attention backward with Context Parallelism support.
    """
    from torch.distributed.tensor._ops._matrix_ops import (
        _scaled_dot_product_cudnn_attention_backward_base_strategies,
    )

    mesh = op_schema.get_mesh_from_args(validate=False)
    single_mesh_dim_strategies = (
        _scaled_dot_product_cudnn_attention_backward_base_strategies(op_schema)
    )

    has_attn_bias = op_schema.args_schema[8] is not None
    has_scale = len(op_schema.args_schema) >= 16 and False

    # Context Parallelism: shards on the sequence dim
    cp_sharding_gout: PlacementList = [Shard(SEQ_DIM)] * 3  # grad_q, grad_k, grad_v
    cp_sharding_ginp: PlacementList = [
        Shard(SEQ_DIM)
    ] * 6  # grad_output, q, k, v, output, logsumexp
    cp_sharding_ginp += [Replicate()] * 2  # philox_seed, philox_offset
    cp_sharding_ginp += [Shard(SEQ_DIM) if has_attn_bias else None]  # attn_bias
    cp_sharding_ginp += [
        None
    ] * 6  # cum_seq_q, cum_seq_k, max_q, max_k, dropout_p, is_causal
    if has_scale:
        cp_sharding_ginp.append(None)

    cp_sharding = cp_sharding_gout + cp_sharding_ginp
    single_mesh_dim_strategies.append(cp_sharding)

    return expand_to_full_mesh_op_strategy(
        mesh, op_schema, single_mesh_dim_strategies, input_index=3
    )

