
def tree_map_params(
    initable: Union[
        Callable[[base.Params], base.OptState],
        Initable,
    ],
    f: Callable[..., Any],
    state: base.OptState,
    /,
    *rest: Any,
    transform_non_params: Optional[Callable[..., Any]] = None,
    is_leaf: Optional[Callable[[base.Params], bool]] = None,
) -> base.OptState:
  """Apply a callable over all params in the given optimizer state.

  This function exists to help construct partition specs over optimizer
  states, in the case that a partition spec is already known for the parameters.

  For example, the following will replace all optimizer state parameter trees
  with copies of the given partition spec instead. The argument
  `transform_non_params` can be used to replace any remaining fields as
  required, in this case, we replace those fields by None.

  >>> params, specs = jnp.array(0.), jnp.array(0.)  # Trees with the same shape
  >>> opt = optax.sgd(1e-3)
  >>> state = opt.init(params)
  >>> opt_specs = optax.tree_map_params(
  ...     opt,
  ...     lambda _, spec: spec,
  ...     state,
  ...     specs,
  ...     transform_non_params=lambda _: None,
  ...     )

  Args:
    initable: A callable taking parameters and returning an optimizer state, or
      an object with an `init` attribute having the same function.
    f: A callable that will be applied for all copies of the parameter tree
      within this optimizer state.
    state: The optimizer state to map over.
    *rest: Additional arguments, having the same shape as the parameter tree,
      that will be passed to f.
    transform_non_params: An optional function that will be called on all
      non-parameter fields within the optimizer state.
    is_leaf: Passed through to `jax.tree.map`. This makes it possible to ignore
      parts of the parameter tree e.g. when the gradient transformations modify
      the shape of the original pytree, such as for ``optax.masked``.

  Returns:
    The result of applying the function f on all trees in the optimizer's state
    that have the same shape as the parameter tree, along with the given
    optional extra arguments.
  """

  # Cast for pytype checks (no-op for other usages).
  placeholder = cast(base.ArrayTree, _ParamsPlaceholder())

  if isinstance(initable, Initable):
    initable = cast(Initable, initable)  # for pytype checks
    state_with_placeholders = initable.init(placeholder)
  else:
    state_with_placeholders = initable(placeholder)

  def map_params(maybe_placeholder_value, value):
    if isinstance(maybe_placeholder_value, _ParamsPlaceholder):
      return jax.tree.map(f, value, *rest, is_leaf=is_leaf)
    if transform_non_params is not None:
      return transform_non_params(value)
    return value

  return jax.tree.map(
      map_params,
      state_with_placeholders,
      state,
      is_leaf=lambda v: isinstance(v, _ParamsPlaceholder),
  )

