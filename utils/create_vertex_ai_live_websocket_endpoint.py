
def create_vertex_ai_live_websocket_endpoint():
    """
    Create a Vertex AI Live WebSocket endpoint using the new passthrough pattern.

    This demonstrates how to use the create_websocket_passthrough_route function
    for a provider-specific WebSocket endpoint.
    """
    # This would be used like:
    # endpoint_func = create_vertex_ai_live_websocket_endpoint()
    # app.websocket("/vertex_ai/live")(endpoint_func)

    # For now, we'll keep the existing implementation since it has
    # provider-specific logic for Vertex AI credentials and headers
    return vertex_ai_live_websocket_passthrough

