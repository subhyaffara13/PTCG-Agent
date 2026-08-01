
def capture(capsys):
    """Extended `capsys` with context manager and custom equality operators"""
    return Capture(capsys)


def capture(stream='stdout'):
    """builds a context that temporarily replaces the given stream name

    >>> with capture('stdout') as out:
    ...   print ("foo!")
    ... 
    >>> print (out.getvalue())
    foo!

    """
    import sys
    from io import StringIO
    orig = getattr(sys, stream)
    setattr(sys, stream, StringIO())
    try:
        yield getattr(sys, stream)
    finally:
        setattr(sys, stream, orig)


def capture(func):
    """Return the printed output of func().

    ``func`` should be a function without arguments that produces output with
    print statements.

    >>> from sympy.utilities.iterables import capture
    >>> from sympy import pprint
    >>> from sympy.abc import x
    >>> def foo():
    ...     print('hello world!')
    ...
    >>> 'hello' in capture(foo) # foo, not foo()
    True
    >>> capture(lambda: pprint(2/x))
    '2\\n-\\nx\\n'

    """
    from io import StringIO
    import sys

    stdout = sys.stdout
    sys.stdout = file = StringIO()
    try:
        func()
    finally:
        sys.stdout = stdout
    return file.getvalue()


def capture(
  fn: tp.Callable[P, R],
  *var_types: type[variableslib.Variable],
  init: tp.Optional[State] = None,
  method_outputs: tp.Optional[type[variableslib.Variable]] = None
) -> tp.Callable[P, tuple[R, State]]: ...


def capture(
  fn: type[variableslib.Variable],
  *var_types: type[variableslib.Variable],
  init: tp.Optional[State] = None,
  method_outputs: tp.Optional[type[variableslib.Variable]] = None
) -> tp.Callable[[tp.Callable[P, R]], tp.Callable[P, tuple[R, State]]]: ...


def capture(fn: tp.Callable[P, R] | type[variableslib.Variable], *var_types: type[variableslib.Variable],
  init : tp.Optional[State] = None,
  method_outputs : tp.Optional[type[variableslib.Variable]] = None
) -> tp.Callable[P, tuple[R, State]] | tp.Callable[[tp.Callable[P, R]], tp.Callable[P, tuple[R, State]]]:
    """Wraps a function to capture intermediate values from a module during execution.

    This function wraps a `Callable`, executing it while collecting intermediate values that were stored using
    ``Module.sow()`` or ``Module.perturb()``.

    The `fn` argument can be either a function, a Module instance, or a bound method.
    If `fn` is a function, its first argument should be the module in which intermediate values are to be recorded.
    If `fn` is a bound method, the module used for storage is inferred from the instance.
    If `fn` is a Module, its `__call__` method will be wrapped.

    Args:
      fn: The `Callable` to wrap.
      var_types: Variable types to capture. If None, defaults to [].
      init: MutableMapping used to initialize perturbation values. This is useful for gradient extraction.
      method_outputs: If provided, automatically sows the output of each method
        in the module and its submodules using this variable type.

    Returns:
      A wrapped function that returns
      a tuple of (result, *intermediates) where result is the output of the function
      and each intermediate is a State containing the captured values with the corresponding type in `var_types`.

    Example with manual sowing::

      class Foo(nnx.Module):
        def __call__(self, x):
          self.sow(nnx.Intermediate, 'features', x)
          return x

      model = Foo(rngs=nnx.Rngs(0))
      forward = nnx.capture(model, nnx.Intermediate)
      result, intermediates = forward(x)
      # intermediates['features'] contains the sowed value

    Example with method outputs::

      class Foo(nnx.Module):
        def features(self, x):
          return x
        def classifier(self, x):
          return x
        def __call__(self, x):
          return self.classifier(self.features(x))

      model = Foo(rngs=nnx.Rngs(0))
      result, intermediates = nnx.capture(
        model, method_output_type=nnx.Intermediate)(x)
      # intermediates contains outputs of features(), classifier(), and __call__()

    Example with gradient extraction::

      class Model(nnx.Module):
        def __call__(self, x):
          x2 = self.perturb('grad_of_x', x)
          return 3 * x2

      model = Model()
      forward = nnx.capture(lambda model, x: model(x), nnx.Perturbation) # Initialize perturbations
      _, perturbations = forward_capture(model, x)

      # Compute gradients with respect to perturbations
      loss = nnx.capture(forward, init=perturbations)
      grads, sowed = nnx.grad(loss, has_aux=True)(model, perturbations, x)
    """

    # Handle partial evaluation when first arg is a Variable type
    if isinstance(fn, type) and issubclass(fn, variableslib.Variable):
      # Partial application: return a function that waits for the actual fn
      all_var_types = (fn,) + var_types
      def partial_capture(actual_fn: tp.Callable[P, R] | Module) -> tp.Callable[P, tuple[R, State]]:
        return capture(actual_fn, *all_var_types, init=init, method_outputs=method_outputs)
      return partial_capture

    # Handle bound methods and callable Modules
    module_instance = None
    if inspect.ismethod(fn) and isinstance(fn.__self__, Module):
      module_instance = fn.__self__
    elif isinstance(fn, Module):
      module_instance = fn

    ft.wraps(fn)
    def wrapper(*fn_args, **kwargs):
      if module_instance is None:
        module = fn_args[0]
      else:
        module = module_instance

      # Extract initial values from state
      state_by_path = _collect_state_by_path(init) if init else {}

      # Initialize __captures__ as a tuple of Variables (one per type)
      for path, m in iter_modules(module):
        # Create initial dicts for each variable type
        initial_dicts = {}
        for var_type in var_types:
          initial_dicts[var_type] = {}

        # Populate from state if available
        if path in state_by_path:
          for name, var in state_by_path[path].items():
            var_type = type(var)
            if var_type not in initial_dicts:
              initial_dicts[var_type] = {}
            initial_dicts[var_type][name] = var.get_value()

        # Create the captures tuple
        captures_tuple = tuple(k(v) for (k,v) in initial_dicts.items())
        m.__captures__ = pytreelib.data(captures_tuple)

      # Wrap methods with capturing if required
      if method_outputs:
        for _, m in iter_modules(module):
          _add_capturing(type(m), method_outputs)

      try:
        result = fn(*fn_args, **kwargs)
      finally:

        # Undo method sowing modification
        for _, m in iter_modules(module):
          _remove_capturing(type(m))

      # Extract intermediates manually from __captures__
      interms = State({})
      _extract_captures(module, interms, set(var_types))
      if len(var_types) == 0:
          return result
      split_states = split_state(interms, *var_types)
      if len(var_types) == 1:
        return result, split_states
      else:
        return (result, *split_states)

    return wrapper

