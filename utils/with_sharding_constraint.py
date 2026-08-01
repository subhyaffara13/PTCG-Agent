
def with_sharding_constraint(x, shardings):
  """Mechanism to constrain the sharding of an Array inside a jitted computation

  This is a strict constraint for the GSPMD partitioner and not a hint. For examples
  of how to use this function, see `Distributed arrays and automatic parallelization`_.

  Inside of a jitted computation, with_sharding_constraint makes it possible to
  constrain intermediate values to an uneven sharding. However, if such an
  unevenly sharded value is output by the jitted computation, it will come out
  as fully replicated, no matter the sharding annotation given.

  Args:
    x: PyTree of jax.Arrays which will have their shardings constrained
    shardings: PyTree of sharding specifications. Valid values are the same as for
      the ``in_shardings`` argument of :func:`jax.experimental.pjit`.
  Returns:
    x_with_shardings: PyTree of jax.Arrays with specified sharding constraints.

  .. _Distributed arrays and automatic parallelization: https://docs.jax.dev/en/latest/parallel.html
  """
  x_flat, tree = tree_flatten(x)
  x_avals_flat = [core.shaped_abstractify(x) for x in x_flat]
  layouts, shardings = _split_layout_and_sharding(shardings)

  user_shardings = prepare_axis_resources(
      shardings, "shardings", allow_unconstrained_dims=True)
  del shardings

  user_shardings_flat = tuple(
      flatten_axes("with_sharding_constraint shardings", tree, user_shardings))
  del user_shardings

  user_layouts_flat = tuple(
      flatten_axes("with_sharding_constraint layouts", tree, layouts))
  del layouts

  if not mesh_lib.get_concrete_mesh().empty:
    context_mesh = mesh_lib.get_abstract_mesh()
  elif not mesh_lib.get_abstract_mesh().empty:
    context_mesh = mesh_lib.get_abstract_mesh()
  else:
    context_mesh = mesh_lib.thread_resources.env.physical_mesh

  shardings_flat = [_create_sharding_for_array(context_mesh, a, 'shardings',
                                               'with_sharding_constraint')
                    for a in user_shardings_flat]
  for s, u in zip(shardings_flat, user_shardings_flat):
    if isinstance(s, UnspecifiedValue):
      raise ValueError(
          f'One of with_sharding_constraint arguments got sharding {u} which is'
          ' not allowed. Please only pass `jax.sharding.Sharding` instances.')
  del user_shardings_flat

  # TODO(bartchr): remove `unconstrained_dims` after migrating to Shardy. It's
  # already part of the shardings.
  unconstrained_dims = [get_unconstrained_dims(s)
                        if isinstance(s, NamedSharding) else frozenset()
                        for s in shardings_flat]

  pjit_check_aval_sharding(
      shardings_flat, x_avals_flat, ("",) * len(shardings_flat),
      "with_sharding_constraint arguments",
      allow_uneven_sharding=True)
  check_aval_layout_compatibility(user_layouts_flat, x_avals_flat,
                                  ("",) * len(user_layouts_flat),
                                  "with_sharding_constraint arguments")

  outs = []
  for xf, x_aval, s, l, ud in zip(x_flat, x_avals_flat, shardings_flat,
                                  user_layouts_flat, unconstrained_dims):
    if (mesh_lib.get_abstract_mesh().are_all_axes_explicit and l is None and
        isinstance(s, NamedSharding)):
      assert_shardings_equal(x_aval, s)
      outs.append(xf)
    else:
      check_shardings_are_auto(s)
      outs.append(sharding_constraint_p.bind(
          xf, sharding=s, layout=l, context_mesh=context_mesh,
          unconstrained_dims=ud))
  return tree_unflatten(tree, outs)

