
def create_websocket_passthrough_route(
    endpoint: str,
    target: str,
    custom_headers: Optional[dict] = None,
    _forward_headers: Optional[bool] = False,
    dependencies: Optional[List] = None,
    cost_per_request: Optional[float] = None,
):
    """
    Create a WebSocket passthrough route function.

    Args:
        endpoint: The endpoint path (for logging purposes)
        target: The target WebSocket URL (e.g., "wss://api.example.com/ws")
        custom_headers: Custom headers to include in the WebSocket connection
        _forward_headers: Whether to forward incoming headers
        dependencies: FastAPI dependencies to inject

    Returns:
        A WebSocket passthrough function that can be registered with app.websocket()
    """
    from litellm.proxy.auth.user_api_key_auth import user_api_key_auth_websocket

    async def websocket_endpoint_func(
        websocket: WebSocket,
        user_api_key_dict: UserAPIKeyAuth = Depends(user_api_key_auth_websocket),
        **kwargs,  # For additional query parameters
    ):
        """
        WebSocket passthrough endpoint function.

        This function handles the WebSocket connection by:
        1. Accepting the incoming WebSocket connection
        2. Establishing a connection to the target WebSocket
        3. Forwarding messages bidirectionally
        4. Handling connection cleanup
        """
        return await websocket_passthrough_request(
            websocket=websocket,
            target=target,
            custom_headers=custom_headers or {},
            user_api_key_dict=user_api_key_dict,
            forward_headers=_forward_headers,
            endpoint=endpoint,
            cost_per_request=cost_per_request,
            accept_websocket=True,  # Generic usage should accept the WebSocket
        )

    return websocket_endpoint_func

