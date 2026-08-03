import functools

def module_class_lift_transform(
  transform, module_class, *trafo_args, methods=None, **trafo_kwargs
):
  """Module class lift transform."""
  # TODO(marcvanzee): Improve docstrings (#1977).
  # TODO(levskaya): find nicer argument convention for multi-method case?

  # Prepare per-method transform args, kwargs.
  if methods is None:
    # Default case, just transform __call__
    class_trafo_args = {'__call__': (trafo_args, trafo_kwargs)}
  elif isinstance(methods, (list, tuple)):
    # Transform every method in methods with given args, kwargs.
    class_trafo_args = {m: (trafo_args, trafo_kwargs) for m in methods}
  elif isinstance(methods, dict):
    # Pass different trafo args per each method.
    class_trafo_args = {k: ((), v) for k, v in methods.items()}
  else:
    raise ValueError(
      'transform methods argument must be None, tuple, list, or dict.'
    )

  # Handle partially initialized module class constructors.
  if isinstance(module_class, functools.partial) and issubclass(
    module_class.func, Module
  ):
    partial_object = module_class
    module_class = module_class.func
  else:
    partial_object = None

  def create_trans_fn(fn_name, fn_trafo_args):
    # get existing unbound method from class
    fn = getattr(module_class, fn_name)
    trafo_args, trafo_kwargs = fn_trafo_args

    # we need to create a scope-function from our class for the given method
    @functools.wraps(fn)
    def wrapped_fn(self, *args, **kwargs):
      state = self._state.export()

      # make a scope-function to transform
      def core_fn(scopes, *args, **kwargs):
        # make a clone of self using its arguments
        attrs = {
          f.name: getattr(self, f.name)
          for f in dataclasses.fields(self)
          if f.name != 'parent' and f.init
        }
        # we reference module_class, not self.__class__ to avoid infinite loop
        cloned = module_class(parent=None, **attrs)
        cloned, args, kwargs = set_module_scopes(cloned, args, kwargs, scopes)
        object.__setattr__(cloned, '_state', state.export())
        res = fn(cloned, *args, **kwargs)
        self._state.reimport(cloned._state)
        _test_transformed_return_values(res, fn_name)
        return res

      # here we apply the given lifting transform to the scope-ingesting fn
      trafo_fn = transform(core_fn, *trafo_args, **trafo_kwargs)
      module_scopes, args, kwargs = get_module_scopes(self, args, kwargs)
      ret = trafo_fn(module_scopes, *args, **kwargs)
      return ret

    return wrapped_fn

  transformed_fns = {
    fn_name: create_trans_fn(fn_name, fn_trafo_args)
    for fn_name, fn_trafo_args in class_trafo_args.items()
  }
  # construct new dynamic class w. transformed methods
  transformed_cls = type(
    transform.__name__.capitalize() + module_class.__name__,
    (module_class,),
    transformed_fns,
  )
  # Handle partially initialized module class constructors.
  if partial_object is not None:
    transformed_cls = functools.partial(
      transformed_cls, *partial_object.args, **partial_object.keywords
    )
  return transformed_cls

