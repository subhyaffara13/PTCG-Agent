import json

def extern_node_json_serializer(
    extern_kernel_nodes: list[inductor_ExternKernelNode],
) -> str:
    serialized_nodes = ExternKernelNodes(
        nodes=[serialize_extern_kernel_node(node) for node in extern_kernel_nodes]
    )
    return json.dumps(_dataclass_to_dict(serialized_nodes), cls=EnumEncoder)

