import copy
import functools
from typing import Any, Callable

def _get_option(target_obj: Distribution | DistributionMetadata, key: str):
    """
    Given a target object and option key, get that option from
    the target object, either through a get_{key} method or
    from an attribute directly.
    """
    getter_name = f'get_{key}'
    by_attribute = functools.partial(getattr, target_obj, key)
    getter = getattr(target_obj, getter_name, by_attribute)
    return getter()


def _get_option(
    opt_value: Any,
    parent_opt: Any,
    default_factory: Callable[[], Any],
) -> Any:
  """Resolves a configuration option dataclass during Context initialization.

  Enforces the following order of precedence:
    1. Direct keyword argument (`opt_value`): Returns a deep copy to insulate
      the context from external mutation.
    2. Parent inheritance (`parent_opt`): Returns a deep copy of the parent's
      option dataclass, ensuring the new child context is fully insulated from
      any future mutations to the parent context (and vice versa).
    3. Fallback (`default_factory`): Creates a fresh default instance.

  Args:
    opt_value: An explicitly provided option dataclass instance, or None.
    parent_opt: The corresponding option dataclass from a parent Context, or
      None.
    default_factory: A callable that produces a fresh default option instance.

  Returns:
    The resolved option dataclass instance.
  """
  if opt_value is not None:
    return copy.deepcopy(opt_value)
  if parent_opt is not None:
    return copy.deepcopy(parent_opt)
  return default_factory()

