
def grpc_error_to_litellm_exception(error: Exception) -> NvidiaRivaException:
    """
    Convert a gRPC error (or any exception raised from the Riva client) into
    a ``NvidiaRivaException`` with an appropriate HTTP-equivalent status code.
    """
    status_name = _extract_grpc_status_name(error)
    http_status = _GRPC_STATUS_CODE_TO_HTTP.get(status_name or "", 500)

    detail = _extract_grpc_details(error) or str(error)
    message = (
        f"NVIDIA Riva gRPC error ({status_name}): {detail}"
        if status_name
        else f"NVIDIA Riva error: {detail}"
    )
    return NvidiaRivaException(status_code=http_status, message=message)

