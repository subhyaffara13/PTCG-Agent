import functools

def async_wrapper(func, obj=None, semaphore=None):
    """
    Wraps a synchronous function to make it awaitable.

    Parameters
    ----------
    func : callable
        The synchronous function to wrap.
    obj : object, optional
        The instance to bind the function to, if applicable.
    semaphore : asyncio.Semaphore, optional
        A semaphore to limit concurrent calls.

    Returns
    -------
    coroutine
        An awaitable version of the function.
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        if semaphore:
            async with semaphore:
                return await asyncio.to_thread(func, *args, **kwargs)
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper

