
def scaled_dot_product_efficient_attention_backward_strategy(
    op_schema: OpSchema,
) -> OpStrategy:
    # backward op does not need to validate the mesh since forward op has already done it
    mesh = op_schema.get_mesh_from_args(validate=False)
    single_mesh_dim_strategies = (
        _scaled_dot_product_efficient_attention_backward_base_strategies(op_schema)
    )
    return expand_to_full_mesh_op_strategy(
        mesh,
        op_schema,
        single_mesh_dim_strategies,
        input_index=4,
    )

