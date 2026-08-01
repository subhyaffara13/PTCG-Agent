
def check_key_reuse(fun: Callable[..., Any], /, *args: Any) -> None:
  """Function to statically check key reuse."""
  function_type_signature(fun, *args)

