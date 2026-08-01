
def _get_input_node_fqn(input_name: str, graph_signature: ExportGraphSignature) -> str:
    """
    Return the FQN of an input node.
    """
    if input_name in graph_signature.inputs_to_parameters:
        return graph_signature.inputs_to_parameters[input_name]
    elif input_name in graph_signature.inputs_to_buffers:
        return graph_signature.inputs_to_buffers[input_name]
    else:
        raise ValueError(
            f"{input_name} not found in inputs_to_parameters or inputs_to_buffers"
        )

