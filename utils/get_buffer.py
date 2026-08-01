
def get_buffer(
    program: "ExportedProgram",
    node: torch.fx.Node,
) -> torch.Tensor | None:
    """
    Returns the buffer associated with the given node in the exported program.
    Returns None if the node is not a buffer within the exported program
    """

    if is_buffer(program, node):
        buffer_name = program.graph_signature.inputs_to_buffers[node.name]
        if buffer_name in program.graph_signature.non_persistent_buffers:
            return program.constants[buffer_name]
        else:
            return program.state_dict[buffer_name]

    return None

