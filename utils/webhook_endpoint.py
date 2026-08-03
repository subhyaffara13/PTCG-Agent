from typing import Callable

def webhook_endpoint(path: str | None = None) -> Callable:
    """Decorator to start a [`WebhooksServer`] and register the decorated function as a webhook endpoint.

    This is a helper to get started quickly. If you need more flexibility (custom landing page or webhook secret),
    you can use [`WebhooksServer`] directly. You can register multiple webhook endpoints (to the same server) by using
    this decorator multiple times.

    Check out the [webhooks guide](../guides/webhooks_server) for a step-by-step tutorial on how to set up your
    server and deploy it on a Space.

    > [!WARNING]
    > `webhook_endpoint` is experimental. Its API is subject to change in the future.

    > [!WARNING]
    > You must have `gradio` installed to use `webhook_endpoint` (`pip install --upgrade gradio`).

    Args:
        path (`str`, optional):
            The URL path to register the webhook function. If not provided, the function name will be used as the path.
            In any case, all webhooks are registered under `/webhooks`.

    Examples:
        The default usage is to register a function as a webhook endpoint. The function name will be used as the path.
        The server will be started automatically at exit (i.e. at the end of the script).

        ```python
        from huggingface_hub import webhook_endpoint, WebhookPayload

        @webhook_endpoint
        async def trigger_training(payload: WebhookPayload):
            if payload.repo.type == "dataset" and payload.event.action == "update":
                # Trigger a training job if a dataset is updated
                ...

        # Server is automatically started at the end of the script.
        ```

        Advanced usage: register a function as a webhook endpoint and start the server manually. This is useful if you
        are running it in a notebook.

        ```python
        from huggingface_hub import webhook_endpoint, WebhookPayload

        @webhook_endpoint
        async def trigger_training(payload: WebhookPayload):
            if payload.repo.type == "dataset" and payload.event.action == "update":
                # Trigger a training job if a dataset is updated
                ...

        # Start the server manually
        trigger_training.launch()
        ```
    """
    if callable(path):
        # If path is a function, it means it was used as a decorator without arguments
        return webhook_endpoint()(path)

    @wraps(WebhooksServer.add_webhook)
    def _inner(func: Callable) -> Callable:
        app = _get_global_app()
        app.add_webhook(path)(func)
        if len(app.registered_webhooks) == 1:
            # Register `app.launch` to run at exit (only once)
            atexit.register(app.launch)

        @wraps(app.launch)
        def _launch_now():
            # Run the app directly (without waiting atexit)
            atexit.unregister(app.launch)
            app.launch()

        func.launch = _launch_now  # type: ignore
        return func

    return _inner

