
def _scaled_dot_product_efficient_attention_base_strategies(
    op_schema: OpSchema,
) -> list[PlacementList]:
    """Helper that returns list of base placement strategies (without CP)."""
    q_input_strategy = op_schema.args_schema[0]
    if not isinstance(q_input_strategy, OpStrategy):
        raise AssertionError(f"Expected OpStrategy, got {type(q_input_strategy)}")
    # assuming q/k/v have the same shape

    has_attn_bias = op_schema.args_schema[3] is not None
    compute_log_sumexp = op_schema.args_schema[4]

    single_mesh_dim_strategies: list[PlacementList] = []

    # placement list stores placements of [outputs, inputs]
    # in the spda case, we have 2 valid tensor outputs and 3 or 4 tensor inputs
    # first we can always accept full replication for both inputs and outputs
    all_replicate: PlacementList = [
        Replicate(),
        Replicate(),
        None,
        None,
        Replicate(),
        Replicate(),
        Replicate(),
    ]
    if has_attn_bias:
        all_replicate.append(Replicate())  # attn bias

    single_mesh_dim_strategies.append(all_replicate)

    # second we can accept the sharding pattern of tensor parallelism, which
    # shard on the heads dimension
    qkv_sharding = Shard(1)
    output_sharding = Shard(1)
    if compute_log_sumexp:
        logsumexp_sharding: Placement = Shard(1)
    else:
        # empty logsumexp, replicated
        logsumexp_sharding = Replicate()

    num_heads_dim_sharding = [
        output_sharding,
        logsumexp_sharding,
        None,
        None,
        qkv_sharding,
        qkv_sharding,
        qkv_sharding,
    ]
    if has_attn_bias:
        num_heads_dim_sharding.append(Shard(1))
    single_mesh_dim_strategies.append(num_heads_dim_sharding)

    # batch sharding
    if compute_log_sumexp:
        logsumexp_sharding_dp: Placement = Shard(0)
    else:
        # empty logsumexp, replicated
        logsumexp_sharding_dp = Replicate()
    batch_sharding = [
        Shard(0),  # output
        logsumexp_sharding_dp,  # logsumexp
        None,  # philox_seed
        None,  # philox_offset
        Shard(0),  # q
        Shard(0),  # k
        Shard(0),  # v
    ]
    if has_attn_bias:
        batch_sharding.append(Shard(0))

    single_mesh_dim_strategies.append(batch_sharding)

    return single_mesh_dim_strategies

