
def _wrap_webhook_to_check_secret(func: Callable, webhook_secret: str) -> Callable:
    """Wraps a webhook function to check the webhook secret before calling the function.

    This is a hacky way to add the `request` parameter to the function signature. Since FastAPI based itself on route
    parameters to inject the values to the function, we need to hack the function signature to retrieve the `Request`
    object (and hence the headers). A far cleaner solution would be to use a middleware. However, since
    `fastapi==0.90.1`, a middleware cannot be added once the app has started. And since the FastAPI app is started by
    Gradio internals (and not by us), we cannot add a middleware.

    This method is called only when a secret has been defined by the user. If a request is sent without the
    "x-webhook-secret", the function will return a 401 error (unauthorized). If the header is sent but is incorrect,
    the function will return a 403 error (forbidden).

    Inspired by https://stackoverflow.com/a/33112180.
    """
    initial_sig = inspect.signature(func)

    @wraps(func)
    async def _protected_func(request: Request, **kwargs):
        request_secret = request.headers.get("x-webhook-secret")
        if request_secret is None:
            return JSONResponse({"error": "x-webhook-secret header not set."}, status_code=401)
        if request_secret != webhook_secret:
            return JSONResponse({"error": "Invalid webhook secret."}, status_code=403)

        # Inject `request` in kwargs if required
        if "request" in initial_sig.parameters:
            kwargs["request"] = request

        # Handle both sync and async routes
        if inspect.iscoroutinefunction(func):
            return await func(**kwargs)
        else:
            return func(**kwargs)

    # Update signature to include request
    if "request" not in initial_sig.parameters:
        _protected_func.__signature__ = initial_sig.replace(  # type: ignore
            parameters=(
                inspect.Parameter(name="request", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=Request),
            )
            + tuple(initial_sig.parameters.values())
        )

    # Return protected route
    return _protected_func

