
def default_async_client_factory() -> httpx.AsyncClient:
    """
    Factory function to create a `httpx.AsyncClient` with the default transport.
    """
    return httpx.AsyncClient(
        event_hooks={"request": [async_hf_request_event_hook], "response": [async_hf_response_event_hook]},
        follow_redirects=True,
        timeout=None,
    )

