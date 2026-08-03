from typing import Any

def ensure_arraylike(fun_name: str, /) -> tuple[()]:
  ...


def ensure_arraylike(fun_name: str, a1: Any, /) -> Array:
  ...


def ensure_arraylike(fun_name: str, a1: Any, a2: Any, /) -> tuple[Array, Array]:
  ...


def ensure_arraylike(fun_name: str, a1: Any, a2: Any, a3: Any, /) -> tuple[Array, Array, Array]:
  ...


def ensure_arraylike(fun_name: str, a1: Any, a2: Any, a3: Any, a4: Any, /, *args: Any) -> tuple[Array, ...]:
  ...


def ensure_arraylike(fun_name: str, /, *args: Any) -> Array | tuple[Array, ...]:
  """Check that arguments are arraylike and convert them to arrays."""
  check_arraylike(fun_name, *args)
  if len(args) == 1:
    return _arraylike_asarray(args[0])
  return tuple(_arraylike_asarray(arg) for arg in args)

