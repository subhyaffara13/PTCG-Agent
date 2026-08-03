import functools

def decorator_lift_transform(
  transform, class_fn, *trafo_args, multi_scope=True, **trafo_kwargs
):
  """Decorator for lifted transform."""
  # TODO(marcvanzee): Improve docstrings (#1977).
  # Due to the ordering of method decorators, we must wrap the class_fn
  # with the module state management wrapper first to maintain Module state
  # correctly.
  if isinstance(class_fn, tuple):
    class_fns = class_fn
  else:
    class_fns = (class_fn,)
  prewrapped_fns = [wrap_method_once(class_fn) for class_fn in class_fns]

  @functools.wraps(prewrapped_fns[0])
  def wrapped_fn(self: Module, *args, **kwargs):
    state = self._state.export()

    # make a scope-function to transform
    def core_fn(prewrapped_fn, class_fn, scopes, *args, **kwargs):
      if not multi_scope:
        scopes = [scopes]
      cloned, args, kwargs = set_module_scopes(self, args, kwargs, scopes)
      object.__setattr__(cloned, '_state', state.export())
      res = prewrapped_fn(cloned, *args, **kwargs)
      self._state.reimport(cloned._state)
      _test_transformed_return_values(res, getattr(class_fn, '__name__', None))
      return res

    core_fns = [
      functools.partial(core_fn, prewrapped_fn, class_fn)
      for prewrapped_fn, class_fn in zip(prewrapped_fns, class_fns)
    ]
    # here we apply the given lifting transform to the scope-ingesting fn
    trafo_fn = transform(*core_fns, *trafo_args, **trafo_kwargs)
    module_scopes, args, kwargs = get_module_scopes(self, args, kwargs)
    if not multi_scope:
      if len(module_scopes) != 1:
        # TODO(levskaya): transforms like jvp & vjp have args that follow the
        # pytree structure of scopes. The user doesn't explicitly control shared
        # modules passed as arguments to methods or as attributes to Module
        # constructors. Therefore, there is no obvious API for specifying
        # arguments per lifted Module.
        raise NotImplementedError(
          'This transform does not yet support'
          ' Modules that include other Modules passed as arguments.'
        )
      module_scopes = module_scopes[0]
    return trafo_fn(module_scopes, *args, **kwargs)

  return wrapped_fn

