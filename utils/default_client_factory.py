
def default_client_factory() -> httpx.Client:
    """
    Factory function to create a `httpx.Client` with the default transport.
    """
    return httpx.Client(
        event_hooks={"request": [hf_request_event_hook]},
        follow_redirects=True,
        timeout=None,
    )

