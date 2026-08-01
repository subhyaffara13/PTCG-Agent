
def bind(optional: _T | None, fn: Callable[[_T], _R]) -> _R | None:
    if optional is None:
        return None
    return fn(optional)


def bind(
  variables: VariableDict,
  rngs: RNGSequences | None = None,
  mutable: CollectionFilter = False,
  flags: Mapping | None = None,
):
  """Binds variables and rngs to a new ``Scope``.

  bind provides a ``Scope`` instance without transforming a function with
  ``apply``. This is particularly useful for debugging and interactive use cases
  like notebooks where a function would limit the ability split up code into
  different cells.

  a ``Scope`` instance is a stateful object. Note that idiomatic JAX is
  functional and therefore a ``Scope` does not mix well well with vanilla JAX
  APIs. Therefore, we recommend using ``apply`` when code should be reusable and
  compatible across the JAX software ecosystem.

  Args:
    variables: Variable dictionary to bind.
    rngs: RNGs to bind.
    mutable: Which variable collections to treat as mutable.
    flags: internal flags.

  Returns:
    A new scope with the variables and rngs bound to it.
  """
  if not _is_valid_variables(variables):
    raise errors.ApplyScopeInvalidVariablesTypeError()
  if rngs is not None and not _is_valid_rngs(rngs):
    raise errors.InvalidRngError(
      'rngs should be a dictionary mapping strings to `jax.PRNGKey`.'
    )
  new_variables = _unfreeze_variables(variables, mutable)
  return Scope(new_variables, rngs=rngs, mutable=mutable, flags=flags)

