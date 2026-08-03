from typing import Any

def _verify_params_are_hashable(
    primitive: core.Primitive, params: dict[str, Any]) -> None:
  for k, v in params.items():
    try:
      hash(v)
    except TypeError as e:
      raise TypeError(
        "As of JAX v0.7, parameters to jaxpr equations must have __hash__ and "
        f"__eq__ methods. In a call to primitive {primitive}, the value of "
        f"parameter {k} was not hashable: {v}") from e

