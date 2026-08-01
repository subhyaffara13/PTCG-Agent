
def run_sync(
    func: Callable[[Unpack[PosArgsT]], T_Retval],
    *args: Unpack[PosArgsT],
    token: EventLoopToken | None = None,
) -> T_Retval:
    """
    Call a function in the event loop thread from a worker thread.

    :param func: a callable
    :param args: positional arguments for the callable
    :param token: an event loop token to use to get back to the event loop thread
        (required if calling this function from outside an AnyIO worker thread)
    :return: the return value of the callable
    :raises MissingTokenError: if no token was provided and called from outside an
        AnyIO worker thread
    :raises RunFinishedError: if the event loop tied to ``token`` is no longer running

    .. versionchanged:: 4.11.0
        Added the ``token`` parameter.

    """
    explicit_token = token is not None
    token = _token_or_error(token)
    return token.backend_class.run_sync_from_thread(
        func, args, token=token.native_token if explicit_token else None
    )


def run_sync(coro: Coroutine[Any, Any, _T]) -> _T:
  """Runs a coroutine and returns the result."""
  try:
    # no event loop: ~0.001s, otherwise: ~0.182s
    loop = asyncio.get_running_loop()
  except RuntimeError:
    loop = None

  if loop is None:
    # No event loop is running, so we can safely use asyncio.run.
    return asyncio.run(coro)
  else:
    # An event loop is already running.
    if uvloop is None:
      if nest_asyncio is None:
        raise RuntimeError(
            'nest_asyncio is not installed. Please install it to use run_sync'
            ' with an existing event loop.'
        )
      nest_asyncio.apply()
      return asyncio.run(coro)
    else:
      event_loop = uvloop.new_event_loop()
      thread = threading.Thread(
          target=_run_event_loop, args=(event_loop,), daemon=True
      )
      thread.start()
      try:
        return asyncio.run_coroutine_threadsafe(coro, event_loop).result()
      finally:
        event_loop.call_soon_threadsafe(event_loop.stop)
        thread.join()


def run_sync(coro: Callable[..., Awaitable[T]]) -> Callable[..., T]:
    """Wraps coroutine in a function that blocks until it has executed.

    Parameters
    ----------
    coro : coroutine-function
        The coroutine-function to be executed.

    Returns
    -------
    result :
        Whatever the coroutine-function returns.
    """

    assert inspect.iscoroutinefunction(coro)

    def wrapped(*args: Any, **kwargs: Any) -> Any:
        name = threading.current_thread().name
        inner = coro(*args, **kwargs)

        loop_running = False
        try:
            asyncio.get_running_loop()
            loop_running = True
        except RuntimeError:
            pass

        if not loop_running:
            # No loop running, run the loop for this thread.
            loop = ensure_event_loop()
            return loop.run_until_complete(inner)

        # Loop is currently running in this thread,
        # use a task runner.
        if name not in _runner_map:
            _runner_map[name] = _TaskRunner()
        return _runner_map[name].run(inner)

    wrapped.__doc__ = coro.__doc__
    return wrapped

