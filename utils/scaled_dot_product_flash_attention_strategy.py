
def scaled_dot_product_flash_attention_strategy(op_schema: OpSchema) -> OpStrategy:
    # NOTE: currently we only support some simple strategies to support tensor parallelism
    # TODO: sdpa might be a good candidate for us to explore decomposed sharding propagation
    # as it involves: matmul, pointwise, reduction ops together.

    mesh = op_schema.get_mesh_from_args()
    single_mesh_dim_strategies = _scaled_dot_product_flash_attention_base_strategies(
        op_schema
    )
    return expand_to_full_mesh_op_strategy(
        mesh, op_schema, single_mesh_dim_strategies, input_index=9
    )

