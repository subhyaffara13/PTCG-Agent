
def serialize_extern_kernel_node(
    extern_kernel_node: inductor_ExternKernelNode,
) -> ExternKernelNode:
    assert isinstance(extern_kernel_node.node, Node)
    return ExternKernelNode(
        name=extern_kernel_node.name,
        node=extern_kernel_node.node,
    )

