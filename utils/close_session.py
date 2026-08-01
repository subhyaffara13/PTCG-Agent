
def close_session() -> None:
    """
    Close the global `httpx.Client` used by `huggingface_hub`.

    If a Client is closed, it will be recreated on the next call to [`get_session`].

    Can be useful if e.g. an SSL certificate has been updated.
    """
    global _GLOBAL_CLIENT
    client = _GLOBAL_CLIENT

    # First, set global client to None
    _GLOBAL_CLIENT = None

    # Then, close the clients
    if client is not None:
        try:
            client.close()
        except Exception as e:
            logger.warning(f"Error closing client: {e}")

