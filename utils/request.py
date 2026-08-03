import json
import sys
from typing import Any, Optional

def request(
    method: bytes | str,
    url: URL | bytes | str,
    *,
    headers: HeaderTypes = None,
    content: bytes | typing.Iterator[bytes] | None = None,
    extensions: Extensions | None = None,
) -> Response:
    """
    Sends an HTTP request, returning the response.

    ```
    response = httpcore.request("GET", "https://www.example.com/")
    ```

    Arguments:
        method: The HTTP method for the request. Typically one of `"GET"`,
            `"OPTIONS"`, `"HEAD"`, `"POST"`, `"PUT"`, `"PATCH"`, or `"DELETE"`.
        url: The URL of the HTTP request. Either as an instance of `httpcore.URL`,
            or as str/bytes.
        headers: The HTTP request headers. Either as a dictionary of str/bytes,
            or as a list of two-tuples of str/bytes.
        content: The content of the request body. Either as bytes,
            or as a bytes iterator.
        extensions: A dictionary of optional extra information included on the request.
            Possible keys include `"timeout"`.

    Returns:
        An instance of `httpcore.Response`.
    """
    with ConnectionPool() as pool:
        return pool.request(
            method=method,
            url=url,
            headers=headers,
            content=content,
            extensions=extensions,
        )


def request(
    method: str,
    url: URL | str,
    *,
    params: QueryParamTypes | None = None,
    content: RequestContent | None = None,
    data: RequestData | None = None,
    files: RequestFiles | None = None,
    json: typing.Any | None = None,
    headers: HeaderTypes | None = None,
    cookies: CookieTypes | None = None,
    auth: AuthTypes | None = None,
    proxy: ProxyTypes | None = None,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    follow_redirects: bool = False,
    verify: ssl.SSLContext | str | bool = True,
    trust_env: bool = True,
) -> Response:
    """
    Sends an HTTP request.

    **Parameters:**

    * **method** - HTTP method for the new `Request` object: `GET`, `OPTIONS`,
    `HEAD`, `POST`, `PUT`, `PATCH`, or `DELETE`.
    * **url** - URL for the new `Request` object.
    * **params** - *(optional)* Query parameters to include in the URL, as a
    string, dictionary, or sequence of two-tuples.
    * **content** - *(optional)* Binary content to include in the body of the
    request, as bytes or a byte iterator.
    * **data** - *(optional)* Form data to include in the body of the request,
    as a dictionary.
    * **files** - *(optional)* A dictionary of upload files to include in the
    body of the request.
    * **json** - *(optional)* A JSON serializable object to include in the body
    of the request.
    * **headers** - *(optional)* Dictionary of HTTP headers to include in the
    request.
    * **cookies** - *(optional)* Dictionary of Cookie items to include in the
    request.
    * **auth** - *(optional)* An authentication class to use when sending the
    request.
    * **proxy** - *(optional)* A proxy URL where all the traffic should be routed.
    * **timeout** - *(optional)* The timeout configuration to use when sending
    the request.
    * **follow_redirects** - *(optional)* Enables or disables HTTP redirects.
    * **verify** - *(optional)* Either `True` to use an SSL context with the
    default CA bundle, `False` to disable verification, or an instance of
    `ssl.SSLContext` to use a custom context.
    * **trust_env** - *(optional)* Enables or disables usage of environment
    variables for configuration.

    **Returns:** `Response`

    Usage:

    ```
    >>> import httpx
    >>> response = httpx.request('GET', 'https://httpbin.org/get')
    >>> response
    <Response [200 OK]>
    ```
    """
    with Client(
        cookies=cookies,
        proxy=proxy,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
    ) as client:
        return client.request(
            method=method,
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            auth=auth,
            follow_redirects=follow_redirects,
        )


def request(
    method: str, url: _t.UriType, **kwargs: Unpack[_t.RequestKwargs]
) -> Response:
    """Constructs and sends a :class:`Request <Request>`.

    :param method: method for the new :class:`Request` object: ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
    :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
    :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
        ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
        or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content_type'`` is a string
        defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
        to add for the file.
    :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
    :param timeout: (optional) How many seconds to wait for the server to send data
        before giving up, as a float, or a :ref:`(connect timeout, read
        timeout) <timeouts>` tuple.
    :type timeout: float or tuple
    :param allow_redirects: (optional) Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to ``True``.
    :type allow_redirects: bool
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
    :param stream: (optional) if ``False``, the response content will be immediately downloaded.
    :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response

    Usage::

      >>> import requests
      >>> req = requests.request('GET', 'https://httpbin.org/get')
      >>> req
      <Response [200]>
    """

    # By using the 'with' statement we are sure the session is closed, thus we
    # avoid leaving sockets open which can trigger a ResourceWarning in some
    # cases, and look like a memory leak in others.
    with sessions.Session() as session:
        return session.request(method=method, url=url, **kwargs)


def request(
    method: str,
    url: str,
    *,
    body: _TYPE_BODY | None = None,
    fields: _TYPE_FIELDS | None = None,
    headers: typing.Mapping[str, str] | None = None,
    preload_content: bool | None = True,
    decode_content: bool | None = True,
    redirect: bool | None = True,
    retries: Retry | bool | int | None = None,
    timeout: Timeout | float | int | None = 3,
    json: typing.Any | None = None,
) -> BaseHTTPResponse:
    """
    A convenience, top-level request method. It uses a module-global ``PoolManager`` instance.
    Therefore, its side effects could be shared across dependencies relying on it.
    To avoid side effects create a new ``PoolManager`` instance and use it instead.
    The method does not accept low-level ``**urlopen_kw`` keyword arguments.

    :param method:
        HTTP request method (such as GET, POST, PUT, etc.)

    :param url:
        The URL to perform the request on.

    :param body:
        Data to send in the request body, either :class:`str`, :class:`bytes`,
        an iterable of :class:`str`/:class:`bytes`, or a file-like object.

    :param fields:
        Data to encode and send in the request body.

    :param headers:
        Dictionary of custom headers to send, such as User-Agent,
        If-None-Match, etc.

    :param bool preload_content:
        If True, the response's body will be preloaded into memory.

    :param bool decode_content:
        If True, will attempt to decode the body based on the
        'content-encoding' header.

    :param redirect:
        If True, automatically handle redirects (status codes 301, 302,
        303, 307, 308). Each redirect counts as a retry. Disabling retries
        will disable redirect, too.

    :param retries:
        Configure the number of retries to allow before raising a
        :class:`~urllib3.exceptions.MaxRetryError` exception.

        If ``None`` (default) will retry 3 times, see ``Retry.DEFAULT``. Pass a
        :class:`~urllib3.util.retry.Retry` object for fine-grained control
        over different types of retries.
        Pass an integer number to retry connection errors that many times,
        but no other types of errors. Pass zero to never retry.

        If ``False``, then retries are disabled and any exception is raised
        immediately. Also, instead of raising a MaxRetryError on redirects,
        the redirect response will be returned.

    :type retries: :class:`~urllib3.util.retry.Retry`, False, or an int.

    :param timeout:
        If specified, overrides the default timeout for this one
        request. It may be a float (in seconds) or an instance of
        :class:`urllib3.util.Timeout`.

    :param json:
        Data to encode and send as JSON with UTF-encoded in the request body.
        The ``"Content-Type"`` header will be set to ``"application/json"``
        unless specified otherwise.
    """

    return _DEFAULT_POOL.request(
        method,
        url,
        body=body,
        fields=fields,
        headers=headers,
        preload_content=preload_content,
        decode_content=decode_content,
        redirect=redirect,
        retries=retries,
        timeout=timeout,
        json=json,
    )


def request(method, url, **kwargs):
    """Constructs and sends a :class:`Request <Request>`.

    :param method: method for the new :class:`Request` object: ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
    :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
    :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
        ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
        or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content_type'`` is a string
        defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
        to add for the file.
    :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
    :param timeout: (optional) How many seconds to wait for the server to send data
        before giving up, as a float, or a :ref:`(connect timeout, read
        timeout) <timeouts>` tuple.
    :type timeout: float or tuple
    :param allow_redirects: (optional) Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to ``True``.
    :type allow_redirects: bool
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
    :param stream: (optional) if ``False``, the response content will be immediately downloaded.
    :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response

    Usage::

      >>> import requests
      >>> req = requests.request('GET', 'https://httpbin.org/get')
      >>> req
      <Response [200]>
    """

    # By using the 'with' statement we are sure the session is closed, thus we
    # avoid leaving sockets open which can trigger a ResourceWarning in some
    # cases, and look like a memory leak in others.
    with sessions.Session() as session:
        return session.request(method=method, url=url, **kwargs)


def request(
    method: str,
    url: str,
    *,
    body: _TYPE_BODY | None = None,
    fields: _TYPE_FIELDS | None = None,
    headers: typing.Mapping[str, str] | None = None,
    preload_content: bool | None = True,
    decode_content: bool | None = True,
    redirect: bool | None = True,
    retries: Retry | bool | int | None = None,
    timeout: Timeout | float | int | None = 3,
    json: typing.Any | None = None,
) -> BaseHTTPResponse:
    """
    A convenience, top-level request method. It uses a module-global ``PoolManager`` instance.
    Therefore, its side effects could be shared across dependencies relying on it.
    To avoid side effects create a new ``PoolManager`` instance and use it instead.
    The method does not accept low-level ``**urlopen_kw`` keyword arguments.

    :param method:
        HTTP request method (such as GET, POST, PUT, etc.)

    :param url:
        The URL to perform the request on.

    :param body:
        Data to send in the request body, either :class:`str`, :class:`bytes`,
        an iterable of :class:`str`/:class:`bytes`, or a file-like object.

    :param fields:
        Data to encode and send in the request body.

    :param headers:
        Dictionary of custom headers to send, such as User-Agent,
        If-None-Match, etc.

    :param bool preload_content:
        If True, the response's body will be preloaded into memory.

    :param bool decode_content:
        If True, will attempt to decode the body based on the
        'content-encoding' header.

    :param redirect:
        If True, automatically handle redirects (status codes 301, 302,
        303, 307, 308). Each redirect counts as a retry. Disabling retries
        will disable redirect, too.

    :param retries:
        Configure the number of retries to allow before raising a
        :class:`~urllib3.exceptions.MaxRetryError` exception.

        If ``None`` (default) will retry 3 times, see ``Retry.DEFAULT``. Pass a
        :class:`~urllib3.util.retry.Retry` object for fine-grained control
        over different types of retries.
        Pass an integer number to retry connection errors that many times,
        but no other types of errors. Pass zero to never retry.

        If ``False``, then retries are disabled and any exception is raised
        immediately. Also, instead of raising a MaxRetryError on redirects,
        the redirect response will be returned.

    :type retries: :class:`~urllib3.util.retry.Retry`, False, or an int.

    :param timeout:
        If specified, overrides the default timeout for this one
        request. It may be a float (in seconds) or an instance of
        :class:`urllib3.util.Timeout`.

    :param json:
        Data to encode and send as JSON with UTF-encoded in the request body.
        The ``"Content-Type"`` header will be set to ``"application/json"``
        unless specified otherwise.
    """

    return _DEFAULT_POOL.request(
        method,
        url,
        body=body,
        fields=fields,
        headers=headers,
        preload_content=preload_content,
        decode_content=decode_content,
        redirect=redirect,
        retries=retries,
        timeout=timeout,
        json=json,
    )


def request(
    status_file: str, command: str, *, timeout: int | None = None, **kwds: object
) -> dict[str, Any]:
    """Send a request to the daemon.

    Return the JSON dict with the response.

    Raise BadStatus if there is something wrong with the status file
    or if the process whose pid is in the status file has died.

    Return {'error': <message>} if an IPC operation or receive()
    raised OSError.  This covers cases such as connection refused or
    closed prematurely as well as invalid JSON received.
    """
    response: dict[str, str] = {}
    args = dict(kwds)
    args["command"] = command
    # Tell the server whether this request was initiated from a human-facing terminal,
    # so that it can format the type checking output accordingly.
    args["is_tty"] = sys.stdout.isatty() or should_force_color()
    args["terminal_width"] = get_terminal_width()
    _, name = get_status(status_file)
    try:
        with IPCClient(name, timeout) as client:
            send(client, args)

            final = False
            while not final:
                response = receive(client)
                final = bool(response.pop("final", False))
                # Display debugging output written to stdout/stderr in the server process for convenience.
                # This should not be confused with "out" and "err" fields in the response.
                # Those fields hold the output of the "check" command, and are handled in check_output().
                stdout = response.pop("stdout", None)
                if stdout:
                    sys.stdout.write(stdout)
                stderr = response.pop("stderr", None)
                if stderr:
                    sys.stderr.write(stderr)
    except (OSError, IPCException) as err:
        return {"error": str(err)}
    # TODO: Other errors, e.g. ValueError, UnicodeError

    return response


def request(
    ctx: click.Context,
    method: str,
    uri: str,
    data: Optional[str] = None,
    json: Optional[str] = None,
    header: tuple[str, ...] = (),
):
    """Make an HTTP request to the LiteLLM proxy server

    METHOD: HTTP method (GET, POST, PUT, DELETE, etc.)
    URI: URI path (will be appended to base_url)

    Examples:
        litellm http request GET /models
        litellm http request POST /chat/completions -j '{"model": "gpt-4", "messages": [{"role": "user", "content": "Hello"}]}'
        litellm http request GET /health/test_connection -H "X-Custom-Header:value"
    """
    # Parse headers from key:value format
    headers = {}
    for h in header:
        try:
            key, value = h.split(":", 1)
            headers[key.strip()] = value.strip()
        except ValueError:
            raise click.BadParameter(
                f"Invalid header format: {h}. Expected format: 'key:value'"
            )

    # Parse JSON data if provided
    json_data = None
    if json:
        try:
            json_data = json_lib.loads(json)
        except ValueError as e:
            raise click.BadParameter(f"Invalid JSON format: {e}")

    # Parse data if provided
    request_data = None
    if data:
        try:
            request_data = json_lib.loads(data)
        except ValueError:
            # If not JSON, use as raw data
            request_data = data

    client = HTTPClient(ctx.obj["base_url"], ctx.obj["api_key"])
    try:
        response = client.request(
            method=method,
            uri=uri,
            data=request_data,
            json=json_data,
            headers=headers,
        )
        rich.print_json(data=response)
    except requests.exceptions.HTTPError as e:
        click.echo(f"Error: HTTP {e.response.status_code}", err=True)
        try:
            error_body = e.response.json()
            rich.print_json(data=error_body)
        except json_lib.JSONDecodeError:
            click.echo(e.response.text, err=True)
        raise click.Abort()

