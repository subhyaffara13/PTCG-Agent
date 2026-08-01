
def run_async_function(async_function, *args, **kwargs):
    """
    Helper utility to run an async function in a sync context.
    Handles the case where there is an existing event loop running.

    Args:
        async_function (Callable): The async function to run
        *args: Positional arguments to pass to the async function
        **kwargs: Keyword arguments to pass to the async function

    Returns:
        The result of the async function execution

    Example:
        ```python
        async def my_async_func(x, y):
            return x + y

        result = run_async_function(my_async_func, 1, 2)
        ```
    """
    from concurrent.futures import ThreadPoolExecutor

    def run_in_new_loop():
        """Run the coroutine in a new event loop within this thread."""
        new_loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(new_loop)
            return new_loop.run_until_complete(async_function(*args, **kwargs))
        finally:
            new_loop.close()
            asyncio.set_event_loop(None)

    try:
        # First, try to get the current event loop
        _ = asyncio.get_running_loop()
        # If we're already in an event loop, run in a separate thread
        # to avoid nested event loop issues
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(run_in_new_loop)
            return future.result()

    except RuntimeError:
        # No running event loop, we can safely run in this thread
        return run_in_new_loop()

