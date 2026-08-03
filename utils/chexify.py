import functools
import logging
from typing import Any, Callable

def chexify(
    fn: Callable[..., Any],
    async_check: bool = True,
    errors: FrozenSet[checkify.ErrorCategory] = ChexifyChecks.user,
) -> Callable[..., Any]:
  """Wraps a transformed function `fn` to enable Chex value assertions.

  Chex value/runtime assertions access concrete values of tensors (e.g.
  `assert_tree_all_finite`) which are not available during JAX tracing, see
  https://jax.readthedocs.io/en/latest/notebooks/How_JAX_primitives_work.html
  and
  https://jax.readthedocs.io/en/latest/_modules/jax/_src/errors.html#ConcretizationTypeError.

  This wrapper enables them in jitted/pmapped functions by performing a
  specifically designed JAX transformation
  https://jax.readthedocs.io/en/latest/debugging/checkify_guide.html#the-checkify-transformation
  and calling functionalised checks
  https://jax.readthedocs.io/en/latest/_autosummary/jax.experimental.checkify.check.html

  Example:

  .. code::

    @chex.chexify
    @jax.jit
    def logp1_abs_safe(x: chex.Array) -> chex.Array:
      chex.assert_tree_all_finite(x)
      return jnp.log(jnp.abs(x) + 1)

    logp1_abs_safe(jnp.ones(2))  # OK
    logp1_abs_safe(jnp.array([jnp.nan, 3]))  # FAILS
    logp1_abs_safe.wait_checks()

  Note 1: This wrapper allows identifying the first failed assertion in a jitted
  code by printing a pointer to the line where the failed assertion was invoked.
  For getting verbose messages (including concrete tensor values), an unjitted
  version of the code will need to be executed with the same input values. Chex
  does not currently provide tools to help with this.

  Note 2: This wrapper fully supports asynchronous executions
  (see https://jax.readthedocs.io/en/latest/async_dispatch.html).
  To block program execution until asynchronous checks for a _chexified_
  function `fn` complete, call `fn.wait_checks()`. Similarly,
  `chex.block_until_chexify_assertions_complete()` will block program execution
  until _all_ asyncronous checks complete.

  Note 3: Chex automatically selects the backend for executing its assertions
  (i.e. CPU or device accelerator) depending on the program context.

  Note 4: Value assertions can have impact on the performance of a function, see
  https://jax.readthedocs.io/en/latest/debugging/checkify_guide.html#limitations

  Note 5: static assertions, such as `assert_shape` or
  `assert_trees_all_equal_dtypes`, can be called from a jitted function without
  `chexify` wrapper (since they do not access concrete values, only
  shapes and/or dtypes which are available during JAX tracing).

  More examples can be found at
  https://github.com/deepmind/chex/blob/master/chex/_src/asserts_chexify_test.py

  Args:
    fn: A transformed function to wrap.
    async_check: Whether to check errors in the async dispatch mode. See
      https://jax.readthedocs.io/en/latest/async_dispatch.html.
    errors: A set of `checkify.ErrorCategory` values which defines the set of
      enabled checks. By default only explicit ``checks`` are enabled (`user`).
      You can also for example enable NaN and Div-by-0 errors by passing the
      `float` set, or for example combine multiple sets through set
      operations (`float | user`).

  Returns:
    A _chexified_ function, i.e. the one with enabled value assertions.
    The returned function has `wait_checks()` method that blocks the caller
    until all pending async checks complete.
  """
  # Hardware/XLA failures can only happen on the C++ side. They are expected to
  # issue critical errors that will immediately crash the whole program.
  # Nevertheless, Chex sets its own timeout for every chexified XLA comp. to
  # ensure that a program never blocks on Chex side when running in async mode.
  async_timeout = 1800  # 30 minutes

  # Get function name.
  if isinstance(fn, functools.partial):
    func_name = fn.func.__name__
  else:
    func_name = fn.__name__

  if async_check:
    # Spawn a thread for processing blocking calls.
    thread_pool = futures.ThreadPoolExecutor(1, f'async_chex_{func_name}')
    # A deque for futures.
    async_check_futures = collections.deque()

  # Checkification.
  checkified_fn = checkify.checkify(fn, errors=errors)

  @functools.wraps(fn)
  def _chexified_fn(*args, **kwargs):
    if _ai.CHEXIFY_STORAGE.level:
      raise RuntimeError(
          'Nested @chexify wrapping is disallowed. '
          'Make sure that you only wrap the function at the outermost level.')

    if _ai.has_tracers((args, kwargs)):
      raise RuntimeError(
          '@chexify must be applied on top of all (p)jit/pmap transformations'
          ' (otherwise it will result in `UnexpectedTracerError`). If you have'
          ' functions that use value assertions, do not wrap them'
          ' individually -- just wrap the outermost function after'
          ' applying all your JAX transformations. See the example at '
          'https://github.com/google-deepmind/chex#static-and-value-aka-runtime-assertions'  # pylint:disable=line-too-long
      )

    if async_check:
      # Check completed calls.
      while async_check_futures and async_check_futures[0].done():
        _check_error(async_check_futures.popleft().result(async_timeout))

    # Run the checkified function.
    _ai.CHEXIFY_STORAGE.level += 1
    try:
      err, out = checkified_fn(*args, **kwargs)
    finally:
      _ai.CHEXIFY_STORAGE.level -= 1

    # Check errors.
    if async_check:
      # Blocking call is deferred to the thread.
      async_check_futures.append(
          thread_pool.submit(lambda: jax.device_get(err)))
    else:
      # Blocks until `fn`'s outputs are ready.
      _check_error(err)

    return out

  def _wait_checks():
    if async_check:
      while async_check_futures:
        _check_error(async_check_futures.popleft().result(async_timeout))

  # Add a barrier callback to the global storage.
  _ai.CHEXIFY_STORAGE.wait_fns.append(_wait_checks)

  # Add the callback to the chexified funtion's properties.
  if not hasattr(_chexified_fn, 'wait_checks'):
    _chexified_fn.wait_checks = _wait_checks
  else:
    logging.warning(
        "Function %s already defines 'wait_checks' method; "
        'Chex will not redefine it.', func_name)

  return _chexified_fn

