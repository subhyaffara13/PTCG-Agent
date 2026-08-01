
def lift_transform_cached(
    transform, target, *trafo_args, methods=None, **trafo_kwargs
):
  """Applies to class or as a decorator on class fns."""
  # TODO(marcvanzee): Improve docstrings (#1977).
  if _is_module_class(target):
    return module_class_lift_transform_cached(
        transform, target, *trafo_args, methods=methods, **trafo_kwargs
    )
  # we presume this is being used as a function decorator in class definition
  elif callable(target) and not isinstance(target, Module):
    return decorator_lift_transform_cached(
        transform, target, *trafo_args, **trafo_kwargs
    )
  else:
    raise errors.TransformTargetError(target)

