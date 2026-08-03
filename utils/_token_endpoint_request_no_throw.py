import json

def _token_endpoint_request_no_throw(
    request,
    token_uri,
    body,
    access_token=None,
    use_json=False,
    can_retry=True,
    headers=None,
    **kwargs
):
    """Makes a request to the OAuth 2.0 authorization server's token endpoint.
    This function doesn't throw on response errors.

    Args:
        request (google.auth.transport.Request): A callable used to make
            HTTP requests.
        token_uri (str): The OAuth 2.0 authorizations server's token endpoint
            URI.
        body (Mapping[str, str]): The parameters to send in the request body.
        access_token (Optional(str)): The access token needed to make the request.
        use_json (Optional(bool)): Use urlencoded format or json format for the
            content type. The default value is False.
        can_retry (bool): Enable or disable request retry behavior.
        headers (Optional[Mapping[str, str]]): The headers for the request.
        kwargs: Additional arguments passed on to the request method. The
            kwargs will be passed to `requests.request` method, see:
            https://docs.python-requests.org/en/latest/api/#requests.request.
            For example, you can use `cert=("cert_pem_path", "key_pem_path")`
            to set up client side SSL certificate, and use
            `verify="ca_bundle_path"` to set up the CA certificates for sever
            side SSL certificate verification.

    Returns:
        Tuple(bool, Mapping[str, str], Optional[bool]): A boolean indicating
          if the request is successful, a mapping for the JSON-decoded response
          data and in the case of an error a boolean indicating if the error
          is retryable.
    """
    if use_json:
        headers_to_use = {"Content-Type": _JSON_CONTENT_TYPE}
        body = json.dumps(body).encode("utf-8")
    else:
        headers_to_use = {"Content-Type": _URLENCODED_CONTENT_TYPE}
        body = urllib.parse.urlencode(body).encode("utf-8")

    if access_token:
        headers_to_use["Authorization"] = "Bearer {}".format(access_token)

    if headers:
        headers_to_use.update(headers)

    response_data = {}
    retryable_error = False

    retries = _exponential_backoff.ExponentialBackoff()
    for _ in retries:
        response = request(
            method="POST", url=token_uri, headers=headers_to_use, body=body, **kwargs
        )
        response_body = (
            response.data.decode("utf-8")
            if hasattr(response.data, "decode")
            else response.data
        )

        try:
            # response_body should be a JSON
            response_data = json.loads(response_body)
        except ValueError:
            response_data = response_body

        if response.status == http_client.OK:
            return True, response_data, None

        retryable_error = _can_retry(
            status_code=response.status, response_data=response_data
        )

        if not can_retry or not retryable_error:
            return False, response_data, retryable_error

    return False, response_data, retryable_error

