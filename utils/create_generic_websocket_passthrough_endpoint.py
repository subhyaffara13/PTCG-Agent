
def create_generic_websocket_passthrough_endpoint(
    provider: str,
    target_url: str,
    custom_headers: Optional[dict] = None,
    forward_headers: bool = False,
    cost_per_request: Optional[float] = None,
):
    """
    Create a generic WebSocket passthrough endpoint for any provider.

    This demonstrates the new WebSocket passthrough pattern that's similar to
    the HTTP create_pass_through_route function.

    Args:
        provider: The provider name (e.g., "anthropic", "cohere")
        target_url: The target WebSocket URL
        custom_headers: Custom headers to include
        forward_headers: Whether to forward incoming headers

    Returns:
        A WebSocket endpoint function that can be registered with app.websocket()

    Example usage:
        # Create a WebSocket endpoint for Anthropic
        anthropic_ws_func = create_generic_websocket_passthrough_endpoint(
            provider="anthropic",
            target_url="wss://api.anthropic.com/v1/ws",
            custom_headers={"x-api-key": "your-api-key"},
            forward_headers=True
        )

        # Register it in proxy_server.py
        app.websocket("/anthropic/ws")(anthropic_ws_func)
    """
    return create_websocket_passthrough_route(
        endpoint=f"/{provider}/ws",
        target=target_url,
        custom_headers=custom_headers,
        _forward_headers=forward_headers,
        cost_per_request=cost_per_request,
    )

