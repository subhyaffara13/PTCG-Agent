
def make_request_options(
    *,
    query: Query | None = None,
    extra_headers: Headers | None = None,
    extra_query: Query | None = None,
    extra_body: Body | None = None,
    idempotency_key: str | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
    post_parser: PostParser | NotGiven = not_given,
    security: SecurityOptions | None = None,
    synthesize_event_and_data: bool | None = None,
) -> RequestOptions:
    """Create a dict of type RequestOptions without keys of NotGiven values."""
    options: RequestOptions = {}
    if extra_headers is not None:
        options["headers"] = extra_headers

    if extra_body is not None:
        options["extra_json"] = cast(AnyMapping, extra_body)

    if query is not None:
        options["params"] = query

    if extra_query is not None:
        options["params"] = {**options.get("params", {}), **extra_query}

    if not isinstance(timeout, NotGiven):
        options["timeout"] = timeout

    if idempotency_key is not None:
        options["idempotency_key"] = idempotency_key

    if is_given(post_parser):
        # internal
        options["post_parser"] = post_parser  # type: ignore

    if security is not None:
        options["security"] = security

    if synthesize_event_and_data is not None:
        options["synthesize_event_and_data"] = synthesize_event_and_data

    return options

