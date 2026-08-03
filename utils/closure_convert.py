from typing import Any, Callable

def closure_convert(fun: Callable, *example_args) -> tuple[Callable, list[Any]]:
  """Closure conversion utility, for use with higher-order custom derivatives.

  To define custom derivatives such as with ``jax.custom_vjp(f)``, the target
  function ``f`` must take, as formal arguments, all values involved in
  differentiation. If ``f`` is a higher-order function, in that it accepts as an
  argument a Python function ``g``, then values stored away in ``g``'s closure
  will not be visible to the custom derivative rules, and attempts at AD
  involving these values will fail. One way around this is to convert the
  closure by extracting these values, and to pass them as explicit formal
  arguments across the custom derivative boundary. This utility carries out that
  conversion. More precisely, it closure-converts the function ``fun``
  specialized to the types of the arguments given in ``example_args``.

  When we refer here to "values in the closure" of ``fun``, we do not mean the
  values that are captured by Python directly when ``fun`` is defined (e.g. the
  Python objects in ``fun.__closure__``, if the attribute exists). Rather, we
  mean values encountered during the execution of ``fun`` on ``example_args``
  that determine its output. This may include, for instance, arrays captured
  transitively in Python closures, i.e. in the Python closure of functions
  called by ``fun``, the closures of the functions that they call, and so forth.

  The function ``fun`` must be a pure function.

  Example usage::

    def minimize(objective_fn, x0):
      converted_fn, aux_args = closure_convert(objective_fn, x0)
      return _minimize(converted_fn, x0, *aux_args)

    @partial(custom_vjp, nondiff_argnums=(0,))
    def _minimize(objective_fn, x0, *args):
      z = objective_fn(x0, *args)
      # ... find minimizer x_opt ...
      return x_opt

    def fwd(objective_fn, x0, *args):
      y = _minimize(objective_fn, x0, *args)
      return y, (y, args)

    def rev(objective_fn, res, g):
      y, args = res
      y_bar = g
      # ... custom reverse-mode AD ...
      return x0_bar, *args_bars

    _minimize.defvjp(fwd, rev)

  Args:
    fun: Python callable to be converted. Must be a pure function.
    example_args: Arrays, scalars, or (nested) standard Python
      containers (tuples, lists, dicts, namedtuples, i.e., pytrees)
      thereof, used to determine the types of the formal arguments to
      ``fun``. This type-specialized form of ``fun`` is the function
      that will be closure converted.

  Returns:
    A pair comprising (i) a Python callable, accepting the same
    arguments as ``fun`` followed by arguments corresponding to the
    values hoisted from its closure, and (ii) a list of values hoisted
    from the closure.
  """
  flat_args, in_tree = tree_flatten(example_args)
  in_avals = tuple(map(core.typeof, flat_args))
  debug = debug_info("closure_convert", fun, example_args, {})
  if config.check_tracer_leaks.value:
    return _closure_convert_for_avals.__wrapped__(fun, in_tree, in_avals, debug)
  else:
    return _closure_convert_for_avals(fun, in_tree, in_avals, debug)

