
def retry(func: WrappedFn) -> WrappedFn: ...


def retry(
    *,
    sleep: t.Callable[[t.Union[int, float]], t.Awaitable[None]],
    stop: "StopBaseT" = ...,
    wait: "WaitBaseT" = ...,
    retry: "t.Union[RetryBaseT, tasyncio.retry.RetryBaseT]" = ...,
    before: t.Callable[["RetryCallState"], t.Union[None, t.Awaitable[None]]] = ...,
    after: t.Callable[["RetryCallState"], t.Union[None, t.Awaitable[None]]] = ...,
    before_sleep: t.Optional[
        t.Callable[["RetryCallState"], t.Union[None, t.Awaitable[None]]]
    ] = ...,
    reraise: bool = ...,
    retry_error_cls: t.Type["RetryError"] = ...,
    retry_error_callback: t.Optional[
        t.Callable[["RetryCallState"], t.Union[t.Any, t.Awaitable[t.Any]]]
    ] = ...,
) -> _AsyncRetryDecorator: ...


def retry(
    sleep: t.Callable[[t.Union[int, float]], None] = sleep,
    stop: "StopBaseT" = stop_never,
    wait: "WaitBaseT" = wait_none(),
    retry: "t.Union[RetryBaseT, tasyncio.retry.RetryBaseT]" = retry_if_exception_type(),
    before: t.Callable[
        ["RetryCallState"], t.Union[None, t.Awaitable[None]]
    ] = before_nothing,
    after: t.Callable[
        ["RetryCallState"], t.Union[None, t.Awaitable[None]]
    ] = after_nothing,
    before_sleep: t.Optional[
        t.Callable[["RetryCallState"], t.Union[None, t.Awaitable[None]]]
    ] = None,
    reraise: bool = False,
    retry_error_cls: t.Type["RetryError"] = RetryError,
    retry_error_callback: t.Optional[
        t.Callable[["RetryCallState"], t.Union[t.Any, t.Awaitable[t.Any]]]
    ] = None,
) -> t.Callable[[WrappedFn], WrappedFn]: ...


def retry(*dargs: t.Any, **dkw: t.Any) -> t.Any:
    """Wrap a function with a new `Retrying` object.

    :param dargs: positional arguments passed to Retrying object
    :param dkw: keyword arguments passed to the Retrying object
    """
    # support both @retry and @retry() as valid syntax
    if len(dargs) == 1 and callable(dargs[0]):
        return retry()(dargs[0])
    else:

        def wrap(f: WrappedFn) -> WrappedFn:
            if isinstance(f, retry_base):
                warnings.warn(
                    f"Got retry_base instance ({f.__class__.__name__}) as callable argument, "
                    f"this will probably hang indefinitely (did you mean retry={f.__class__.__name__}(...)?)"
                )
            r: "BaseRetrying"
            sleep = dkw.get("sleep")
            if _utils.is_coroutine_callable(f) or (
                sleep is not None and _utils.is_coroutine_callable(sleep)
            ):
                r = AsyncRetrying(*dargs, **dkw)
            elif (
                tornado
                and hasattr(tornado.gen, "is_coroutine_function")
                and tornado.gen.is_coroutine_function(f)
            ):
                r = TornadoRetrying(*dargs, **dkw)
            else:
                r = Retrying(*dargs, **dkw)

            return r.wraps(f)

        return wrap


def retry(
    max_retries=5,
    initial_delay=1.0,
    max_delay=30.0,
    jitter=True,
    exceptions=(Exception,),
):
    """
    Decorator that retries a function call with exponential backoff.

    Args:
        max_retries (`int`, *optional*, defaults to 5):
            Maximum number of retry attempts.
        initial_delay (`float`, *optional*, defaults to 1.0):
            Initial delay in seconds before the first retry.
        max_delay (`float`, *optional*, defaults to 30.0):
            Maximum delay in seconds between retries.
        jitter (`bool`, *optional*, defaults to `True`):
            Whether to add random jitter to the delay.
        exceptions (`tuple`, *optional*, defaults to `(Exception,)`):
            Tuple of exception types to catch and retry on.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay

            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    if attempt == max_retries:
                        raise

                    sleep_for = min(delay, max_delay)
                    if jitter:
                        sleep_for *= random.uniform(0.8, 1.2)

                    logger.info(
                        f"[{func.__name__}] attempt {attempt}/{max_retries} failed: {exc}\n"
                        f"Retrying in {sleep_for:.1f}s..."
                    )
                    time.sleep(sleep_for)
                    delay = min(delay * 2, max_delay)

        return wrapper

    return decorator


def retry(ExceptionToCheck, tries=3, delay=3, skip_after_retries=False):
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    msg = f"{e}, Retrying in {mdelay:d} seconds..."
                    print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
            try:
                return f(*args, **kwargs)
            except ExceptionToCheck as e:
                raise unittest.SkipTest(f"Skipping after {tries} consecutive {str(e)}") from e if skip_after_retries else e
        return f_retry  # true decorator
    return deco_retry


def retry(*r_args, **r_kwargs):
    """
    Decorator wrapper for retry_call. Accepts arguments to retry_call
    except func and then returns a decorator for the decorated function.

    Ex:

    >>> @retry(retries=3)
    ... def my_func(a, b):
    ...     "this is my funk"
    ...     print(a, b)
    >>> my_func.__doc__
    'this is my funk'
    """

    def decorate(func):
        @functools.wraps(func)
        def wrapper(*f_args, **f_kwargs):
            bound = functools.partial(func, *f_args, **f_kwargs)
            return retry_call(bound, *r_args, **r_kwargs)

        return wrapper

    return decorate


def retry(
    wait: float, stop_after_delay: float
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorator to automatically retry a function on error.

    If the function raises, the function is recalled with the same arguments
    until it returns or the time limit is reached. When the time limit is
    surpassed, the last exception raised is reraised.

    :param wait: The time to wait after an error before retrying, in seconds.
    :param stop_after_delay: The time limit after which retries will cease,
        in seconds.
    """

    def wrapper(func: Callable[P, T]) -> Callable[P, T]:

        @functools.wraps(func)
        def retry_wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
            # The performance counter is monotonic on all platforms we care
            # about and has much better resolution than time.monotonic().
            start_time = perf_counter()
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if perf_counter() - start_time > stop_after_delay:
                        raise
                    sleep(wait)

        return retry_wrapped

    return wrapper


def retry(
    func=None,
    initial_delay=0,
    wait=np.logspace(-1, 1, 5) * np.random.rand(5),
    exceptions=Exception,
):
  def retry_decorator(func):
    def retry_driver(*args, **kwargs):
      # Retry the function call with exponential backoff
      for i, t in enumerate(chain([initial_delay], wait)):
        logger.debug(
          f"Trying {func.__name__} in {t:.2f} seconds, attempt {i}/{len(wait)}"
        )
        time.sleep(t)
        try:
          return func(*args, **kwargs)
        except exceptions as e:
          if i == len(wait):
            raise RuntimeError('Retry failed with all attempts exhausted') from e
        finally:
          logger.debug(
            f"Finished {func.__name__} after {i+1} attempts"
          )
    return retry_driver

  if func is None:
    return retry_decorator
  else:
    return retry_decorator(func)

