
def _generate_default_output_sharding(
    node: Node,
    mesh: DeviceMesh,
    op_schema: OpSchema,
) -> OutputSharding:
    """
    Util function to create a default output sharding that suggests Replicate placement for both args and outputs.
    """

    def update_arg_spec(arg_spec: DTensorSpec) -> DTensorSpec:
        return DTensorSpec(
            mesh=arg_spec.mesh,
            placements=(Replicate(),),
            tensor_meta=arg_spec.tensor_meta,
        )

    new_op_schema = OpSchema(
        op=op_schema.op,
        args_schema=pytree.tree_map_only(
            DTensorSpec, update_arg_spec, op_schema.args_schema
        ),
        kwargs_schema=op_schema.kwargs_schema,
    )

    def create_output_spec(tensor: FakeTensor) -> DTensorSpec:
        return DTensorSpec(
            mesh=mesh,
            placements=(Replicate(),),
            tensor_meta=TensorMeta(
                shape=tensor.shape,
                stride=tensor.stride(),
                dtype=tensor.dtype,
            ),
        )

    return OutputSharding(
        output_spec=pytree.tree_map_only(
            FakeTensor, create_output_spec, node.meta["val"]
        ),
        redistribute_schema=new_op_schema,
        needs_redistribute=True,
    )

