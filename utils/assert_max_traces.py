import functools
from typing import Any, Callable, Optional, Union

def assert_max_traces(fn: Optional[Union[Callable[..., Any], int]] = None,
                      n: Optional[Union[Callable[..., Any], int]] = None):
  """Checks that a function is traced at most `n` times (inclusively).

  JAX re-traces jitted functions every time the structure of passed arguments
  changes. Often this behaviour is inadvertent and leads to a significant
  performance drop which is hard to debug. This wrapper checks that
  the function is re-traced at most `n` times during program execution.

  Examples:

  .. code-block:: python

    @jax.jit
    @chex.assert_max_traces(n=1)
    def fn_sum_jitted(x, y):
      return x + y

    def fn_sub(x, y):
      return x - y

    fn_sub_pmapped = jax.pmap(chex.assert_max_retraces(fn_sub), n=10)

  More about tracing:
    https://jax.readthedocs.io/en/latest/notebooks/How_JAX_primitives_work.html

  Args:
    fn: A pure python function to wrap (i.e. it must not be a jitted function).
    n: The maximum allowed number of retraces (non-negative).

  Returns:
    Decorated function that raises exception when it is re-traced `n+1`-st time.

  Raises:
    ValueError: If ``fn`` has already been jitted.
  """
  if not callable(fn) and n is None:
    # Passed n as a first argument.
    n, fn = fn, n

  # Currying.
  if fn is None:
    return lambda fn_: assert_max_traces(fn_, n)

  # Args are expected to be in the right order from here onwards.
  fn = cast(Callable[..., Any], fn)
  n = cast(int, n)
  assert_scalar_non_negative(n)

  # Check wrappers ordering.
  if _ai.is_traceable(fn):
    raise ValueError(
        "@assert_max_traces must not wrap JAX-transformed function "
        "(@jit, @vmap, @pmap etc.); change wrappers ordering.")

  # Footprint is defined as a stacktrace of modules' names at the function's
  # definition place + its name and source code. This allows to catch retracing
  # event both in loops and in sequential calls, and makes this wrapper
  # with Colab envs.
  fn_footprint = (
      tuple(frame.name for frame in traceback.extract_stack()[:-1]) +
      (inspect.getsource(fn), fn.__name__))
  fn_hash = hash(fn_footprint)

  @functools.wraps(fn)
  def fn_wrapped(*args, **kwargs):
    # We assume that a function without arguments is not being traced.
    # That is, case of n=0 for no-arguments function won't raise a error.
    has_tracers_in_args = _ai.has_tracers((args, kwargs))

    _ai.TRACE_COUNTER[fn_hash] += int(has_tracers_in_args)
    if not _ai.DISABLE_ASSERTIONS and _ai.TRACE_COUNTER[fn_hash] > n:
      raise AssertionError(
          f"{_ai.ERR_PREFIX}Function '{fn.__name__}' is traced > {n} times!\n"
          "It often happens when a jitted function is defined inside another "
          "function that is called multiple times (i.e. the jitted f-n is a "
          "new object every time). Make sure that your code does not exploit "
          "this pattern (move the nested functions to the top level to fix it)."
          " See `chex.clear_trace_counter()` if `@chex.assert_max_traces` is "
          "used in any unit tests (especially @parameterized tests).")

    return fn(*args, **kwargs)

  return fn_wrapped

