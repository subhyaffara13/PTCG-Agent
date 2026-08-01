
def _validate_langfuse_proxy_path(endpoint: str) -> str:
    decoded_endpoint = _decode_to_convergence(endpoint)
    if any(ord(char) < 32 for char in decoded_endpoint):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Invalid Langfuse endpoint path"},
        )
    if "\\" in decoded_endpoint or decoded_endpoint.startswith("//"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Invalid Langfuse endpoint path"},
        )

    endpoint_path = "/" + decoded_endpoint.lstrip("/")
    if any(segment in (".", "..") for segment in endpoint_path.split("/")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Invalid Langfuse endpoint path"},
        )
    return endpoint_path

