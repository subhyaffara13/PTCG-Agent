
def is_lifted_tensor_constant(
    program: "ExportedProgram",
    node: torch.fx.Node,
) -> bool:
    """
    Checks if the given node is a lifted tensor constant within the exported program
    """

    return node.name in program.graph_signature.inputs_to_lifted_tensor_constants

