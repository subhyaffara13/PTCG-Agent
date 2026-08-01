
def thread_map(fn, *iterables, **tqdm_kwargs):
    """
    Equivalent of `list(map(fn, *iterables))`
    driven by `concurrent.futures.ThreadPoolExecutor`.

    Parameters
    ----------
    tqdm_class  : optional
        `tqdm` class to use for bars [default: tqdm.auto.tqdm].
    max_workers  : int, optional
        Maximum number of workers to spawn; passed to
        `concurrent.futures.ThreadPoolExecutor.__init__`.
        [default: max(32, cpu_count() + 4)].
    """
    from concurrent.futures import ThreadPoolExecutor
    return _executor_map(ThreadPoolExecutor, fn, *iterables, **tqdm_kwargs)


def thread_map(
    f,
    num_threads,
    token,
    *args,
    use_ordered_callback=False,
    device_id=None,
    on_exception=lambda *args, **kwargs: None):
  """Executes `f(thread_id, token, *args)` for `num_threads` threads."""

  if num_threads == 1:
    # We're running `f` in the same JAX computation as the caller, so we thread
    # the token through.
    return f(jnp.int32(0), token, *args)

  def _f(core_or_thread_index, *args):
    # We are running `f` in sparate JAX computations on different threads from
    # the caller, so there cannot be any jaxpr-level dependencies/ordering
    # between IO callbacks in `f` and in the caller.  We pass a distinct value
    # (instead of the caller's `token`) to make this more clear.
    return f(core_or_thread_index, jnp.int32(NESTED_TOKEN_VALUE), *args)

  jaxpr = jax.make_jaxpr(_f)(jnp.int32(0), *args)

  return _call_threadmap_callback(
      token, device_id, jaxpr.jaxpr, num_threads, jaxpr.consts, args,
      use_ordered_callback, on_exception)

