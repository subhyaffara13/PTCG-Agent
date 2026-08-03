import functools
from typing import Any, Callable

def lift_direct_transform(
  transform: Callable[..., Any],
  targets: tuple[Callable[..., Any], ...],
  mdl: Module,
  *args,
  multi_scope=True,
  **kwargs,
):
  """Lift direct transform."""
  # TODO(marcvanzee): Improve docstrings (#1977).
  for target in targets:
    if _is_module_class(target):
      raise ValueError(
        f'The {transform.__name__} transform can only be applied on a Module'
        ' method. That is function that takes a Module instance as its first'
        ' arg.'
      )
    elif not callable(target):
      raise ValueError('transform target must be callable')
  # normalize self.foo bound methods to class.foo unbound methods.
  targets = tuple(_get_unbound_fn(target) for target in targets)
  aug_transform = lambda *fns: functools.partial(transform, *fns)
  return decorator_lift_transform(
    aug_transform, targets, multi_scope=multi_scope
  )(mdl, *args, **kwargs)

