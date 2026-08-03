from typing import Any, Callable

def make_callable(
    fun: Callable[..., Any],
    fun_sourceinfo: str | None,
    fun_signature: inspect.Signature | None,
):
  return _DEFAULT_FUNCTION_MAKER.make_callable(
      fun, fun_sourceinfo, fun_signature
  )

