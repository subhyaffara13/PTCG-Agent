
def send_jspi_request(
    request: EmscriptenRequest, streaming: bool
) -> EmscriptenResponse:
    """
    Send a request using WebAssembly JavaScript Promise Integration
    to wrap the asynchronous JavaScript fetch api (experimental).

    :param request:
        Request to send

    :param streaming:
        Whether to stream the response

    :return: The response object
    :rtype: EmscriptenResponse
    """
    timeout = request.timeout
    js_abort_controller = js.AbortController.new()
    headers = {k: v for k, v in request.headers.items() if k not in HEADERS_TO_IGNORE}
    req_body = request.body
    fetch_data = {
        "headers": headers,
        "body": to_js(req_body),
        "method": request.method,
        "signal": js_abort_controller.signal,
    }
    # Node.js returns the whole response (unlike opaqueredirect in browsers),
    # so urllib3 can set `redirect: manual` to control redirects itself.
    # https://stackoverflow.com/a/78524615
    if _is_node_js():
        fetch_data["redirect"] = "manual"
    # Call JavaScript fetch (async api, returns a promise)
    fetcher_promise_js = js.fetch(request.url, _obj_from_dict(fetch_data))
    # Now suspend WebAssembly until we resolve that promise
    # or time out.
    response_js = _run_sync_with_timeout(
        fetcher_promise_js,
        timeout,
        js_abort_controller,
        request=request,
        response=None,
    )
    headers = {}
    header_iter = response_js.headers.entries()
    while True:
        iter_value_js = header_iter.next()
        if getattr(iter_value_js, "done", False):
            break
        else:
            headers[str(iter_value_js.value[0])] = str(iter_value_js.value[1])
    status_code = response_js.status
    body: bytes | io.RawIOBase = b""

    response = EmscriptenResponse(
        status_code=status_code, headers=headers, body=b"", request=request
    )
    if streaming:
        # get via inputstream
        if response_js.body is not None:
            # get a reader from the fetch response
            body_stream_js = response_js.body.getReader()
            body = _JSPIReadStream(
                body_stream_js, timeout, request, response, js_abort_controller
            )
    else:
        # get directly via arraybuffer
        # n.b. this is another async JavaScript call.
        body = _run_sync_with_timeout(
            response_js.arrayBuffer(),
            timeout,
            js_abort_controller,
            request=request,
            response=response,
        ).to_py()
    response.body = body
    return response


def send_jspi_request(
    request: EmscriptenRequest, streaming: bool
) -> EmscriptenResponse:
    """
    Send a request using WebAssembly JavaScript Promise Integration
    to wrap the asynchronous JavaScript fetch api (experimental).

    :param request:
        Request to send

    :param streaming:
        Whether to stream the response

    :return: The response object
    :rtype: EmscriptenResponse
    """
    timeout = request.timeout
    js_abort_controller = js.AbortController.new()
    headers = {k: v for k, v in request.headers.items() if k not in HEADERS_TO_IGNORE}
    req_body = request.body
    fetch_data = {
        "headers": headers,
        "body": to_js(req_body),
        "method": request.method,
        "signal": js_abort_controller.signal,
    }
    # Node.js returns the whole response (unlike opaqueredirect in browsers),
    # so urllib3 can set `redirect: manual` to control redirects itself.
    # https://stackoverflow.com/a/78524615
    if _is_node_js():
        fetch_data["redirect"] = "manual"
    # Call JavaScript fetch (async api, returns a promise)
    fetcher_promise_js = js.fetch(request.url, _obj_from_dict(fetch_data))
    # Now suspend WebAssembly until we resolve that promise
    # or time out.
    response_js = _run_sync_with_timeout(
        fetcher_promise_js,
        timeout,
        js_abort_controller,
        request=request,
        response=None,
    )
    headers = {}
    header_iter = response_js.headers.entries()
    while True:
        iter_value_js = header_iter.next()
        if getattr(iter_value_js, "done", False):
            break
        else:
            headers[str(iter_value_js.value[0])] = str(iter_value_js.value[1])
    status_code = response_js.status
    body: bytes | io.RawIOBase = b""

    response = EmscriptenResponse(
        status_code=status_code, headers=headers, body=b"", request=request
    )
    if streaming:
        # get via inputstream
        if response_js.body is not None:
            # get a reader from the fetch response
            body_stream_js = response_js.body.getReader()
            body = _JSPIReadStream(
                body_stream_js, timeout, request, response, js_abort_controller
            )
    else:
        # get directly via arraybuffer
        # n.b. this is another async JavaScript call.
        body = _run_sync_with_timeout(
            response_js.arrayBuffer(),
            timeout,
            js_abort_controller,
            request=request,
            response=response,
        ).to_py()
    response.body = body
    return response

