
def _gen_reshard_suggestions(
    op_schema: OpSchema,
    input_dims: list[str],
    input_specs: tuple[DTensorSpec, ...],
    dim_to_sharding: dict[str, int],
    pending_sum: list[int],
) -> OutputSharding:
    suggested_arg_specs: list[DTensorSpec] = []
    for input_dim, input_spec in zip(input_dims, input_specs):
        dim_map = [dim_to_sharding[dim] for dim in input_dim]
        suggested_arg_specs.append(
            DTensorSpec.from_dim_map(
                mesh=input_spec.mesh,
                dim_map=dim_map,
                sums=pending_sum,
                tensor_meta=input_spec.tensor_meta,
            )
        )
    suggested_schema = OpSchema(op_schema.op, tuple(suggested_arg_specs), {})
    suggested_schema._inplace_rewrap_schema_suggestion(op_schema)
    return OutputSharding(
        None,
        redistribute_schema=suggested_schema,
    )

