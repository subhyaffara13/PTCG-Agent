
def get_vertex_pass_through_handler(
    call_type: Literal["discovery", "aiplatform"],
) -> BaseVertexAIPassThroughHandler:
    if call_type == "discovery":
        return VertexAIDiscoveryPassThroughHandler()
    elif call_type == "aiplatform":
        return VertexAIPassThroughHandler()
    else:
        raise ValueError(f"Invalid call type: {call_type}")

