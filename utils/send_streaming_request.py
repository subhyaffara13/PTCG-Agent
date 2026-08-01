
def send_streaming_request(request: EmscriptenRequest) -> EmscriptenResponse | None:
    if has_jspi():
        return send_jspi_request(request, True)
    elif is_in_node():
        raise _RequestError(
            message=NODE_JSPI_ERROR,
            request=request,
            response=None,
        )

    if _fetcher and streaming_ready():
        return _fetcher.send(request)
    else:
        _show_streaming_warning()
        return None


def send_streaming_request(request: EmscriptenRequest) -> EmscriptenResponse | None:
    if has_jspi():
        return send_jspi_request(request, True)
    elif is_in_node():
        raise _RequestError(
            message=NODE_JSPI_ERROR,
            request=request,
            response=None,
        )

    if _fetcher and streaming_ready():
        return _fetcher.send(request)
    else:
        _show_streaming_warning()
        return None

