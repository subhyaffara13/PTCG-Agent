
def _sharding_constraint_impl(x, sharding, layout, context_mesh,
                              unconstrained_dims):
  if (isinstance(sharding, NamedSharding) and
      isinstance(sharding.mesh, AbstractMesh)):
    if (not context_mesh.empty and isinstance(context_mesh, AbstractMesh) and
        not hasattr(x, 'sharding')):
      concrete_mesh = mesh_lib.get_concrete_mesh()
      assert not concrete_mesh.empty
      sharding = NamedSharding(concrete_mesh, sharding.spec)
    else:
      aval = core.shaped_abstractify(x)
      if not hasattr(x, 'sharding'):
        raise ValueError(
            'Target sharding contains a `jax.sharding.AbstractMesh` which'
            ' requires the input passed should be a `jax.Array`. Got'
            f' {type(x)} with shape {aval.str_short()}')
      if not isinstance(x.sharding, NamedSharding) or x.sharding.mesh.is_scalar:  # pyrefly: ignore[missing-attribute]
        raise TypeError(
            'The sharding on the input must be a `NamedSharding` since the'
            ' target sharding has an `AbstractMesh` in it. Got sharding type'
            f' {type(x.sharding)} for shape {aval.str_short()}')
      if x.sharding.mesh.shape_tuple != sharding.mesh.shape_tuple:
        raise ValueError(
            f'Mesh shape of the input {x.sharding.mesh.shape_tuple} does not'
            ' match the mesh shape of the target sharding'
            f' {sharding.mesh.shape_tuple} for shape {aval.str_short()}')
      sharding = NamedSharding(x.sharding.mesh, sharding.spec)

  if layout is None:
    if mlir.contains_unconstrained(sharding):
      # Can't do identity_jit because UNCONSTRAINED in out_shardings parameter
      # of jit is not supported.
      return dispatch.apply_primitive(
          sharding_constraint_p, x,  sharding=sharding, layout=layout,
          context_mesh=context_mesh, unconstrained_dims=unconstrained_dims)
    else:
      return api.jit(_identity_fn, out_shardings=sharding)(x)
  else:
    return api.jit(_identity_fn, out_shardings=Format(layout, sharding))(x)

