from typing import Callable

def register_xla_runtime_error_handler(
    handler_fn: Callable[[_jax.JaxRuntimeError], Exception | None],
):
  """Registers a custom exception handler for XLA runtime errors.

  Registering a custom handler allows re-raising a more informative exception
  after encountering an XLARuntimeError.

  Args:
    handler_fn: A function which returns a new exception to replace the original
      XLA runtime error, or None if the original error should be propagated.

  Returns:
    A new exception or None.
  """
  _XLA_RUNTIME_ERROR_HANDLERS.append(handler_fn)

