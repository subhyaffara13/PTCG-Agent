
def symbolic_args_specs(
    args,  # pytree of arguments
    shapes_specs,  # prefix pytree of strings
    constraints: Sequence[str] = (),
    scope: SymbolicScope | None = None,
):
  """Constructs a pytree of jax.ShapeDtypeStruct arguments specs for `export`.

  See the documentation of :func:`jax.export.symbolic_shape` and
  the [shape polymorphism documentation](https://docs.jax.dev/en/latest/export/shape_poly.html) for details.

  Args:
    args: a pytree of arguments. These can be jax.Array, or jax.ShapeDtypeStruct.
      They are used to learn the pytree structure of the arguments, their dtypes,
      and to fill-in the actual shapes where the `shapes_specs` contains
      placeholders. Note that only the shape dimensions for which
      `shapes_specs` is a placeholder are used from `args`.
    shapes_specs: should be `None` (all arguments have static shapes),
      a single string (see `shape_spec` for :func:`jax.export.symbolic_shape`;
      applies to all arguments), or a pytree matching a prefix
      of the `args`.
      See [how optional parameters are matched to
      arguments](https://docs.jax.dev/en/latest/pytrees.html#applying-optional-parameters-to-pytrees).
    constraints: as for :func:`jax.export.symbolic_shape`.
    scope: as for :func:`jax.export.symbolic_shape`.

  Returns: a pytree of jax.ShapeDtypeStruct matching the `args` with the shapes
    replaced with symbolic dimensions as specified by `shapes_specs`.
  """
  polymorphic_shapes = shapes_specs
  args_flat, args_tree = tree_util.tree_flatten(args)

  shapes_and_dtypes = tuple(map(shape_and_dtype_jax_array, args_flat))
  shapes, dtypes = util.unzip2(shapes_and_dtypes)

  if isinstance(args, tuple) and isinstance(polymorphic_shapes, list):
    # TODO: Remove backward-compatibility workaround
    polymorphic_shapes_ = tuple(polymorphic_shapes)
  else:
    polymorphic_shapes_ = polymorphic_shapes

  try:
    polymorphic_shapes_flat = tree_util.broadcast_prefix(
        polymorphic_shapes_, args,
        is_leaf=lambda x: x is None)
  except ValueError:
    e, *_ = tree_util.prefix_errors(
        polymorphic_shapes_, args,
        is_leaf=lambda x: x is None)
    raise e("export.symbolic_args_specs shapes_specs") from None

  # Now add in the polymorphic shapes
  if scope is None:
    scope = SymbolicScope(constraints)
  elif constraints:
    raise ValueError("Cannot use both `scope` and `constraints`")
  args_specs_flat = (
      api.ShapeDtypeStruct(symbolic_shape(spec, like=s, scope=scope), t)
      for s, t, spec in zip(shapes, dtypes, polymorphic_shapes_flat))

  return args_tree.unflatten(args_specs_flat)

