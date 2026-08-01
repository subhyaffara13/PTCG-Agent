
def _mpmd_map_batching_rule(
    axis_data,
    args,
    dims,
    *,
    jaxprs,
    meshes,
    out_avals,
    input_output_aliases,
    **params,
):
  if all(d is None for d in dims):
    out = mpmd_map_p.bind(
        *args,
        jaxprs=jaxprs,
        meshes=meshes,
        out_avals=out_avals,
        input_output_aliases=input_output_aliases,
        **params,
    )
    return out, (None,) * len(out)

  for jaxpr in jaxprs:
    for var, dim in zip(jaxpr.invars[: len(args)], dims):
      if (
          not isinstance(var.aval, state.AbstractRef)
          and dim is not None
      ):
        raise ValueError(
            "Closed-over scalar constants cannot be batched. Pass them as"
            " inputs instead."
        )

  if axis_data.size != 1:
    raise NotImplementedError(
        "mpmd_map only supports batching with a batch dimension of 1, got"
        f" {axis_data.size}"
    )

  squeezed_args = []
  for arg, dim in zip(args, dims):
    if dim is None:
      squeezed_args.append(arg)
    elif isinstance(arg_aval := jax_core.typeof(arg), state.AbstractRef):
      # This is a bit of a hack. We rely on the fact that JAX does not have
      # true mutable refs, and thus it is effectively free to squeeze-copy
      # the underlying array like we do below.
      #
      # TODO(slebedev): Add first class support for ``TransformedRef``s to
      # ``mpmd_map`` and get rid of this.
      squeezed_args.append(
          jax_core.new_ref(
              jnp.squeeze(arg[...], dim),
              memory_space=arg_aval.memory_space,
          )
      )
    else:
      squeezed_args.append(jnp.squeeze(arg, dim))

  outs = mpmd_map_p.bind(
      *squeezed_args,
      jaxprs=jaxprs,
      meshes=meshes,
      out_avals=out_avals,
      input_output_aliases=input_output_aliases,
      **params,
  )

  for arg, squeezed_arg, dim in zip(args, squeezed_args, dims):
    if dim is None:
      continue
    if isinstance(jax_core.typeof(arg), state.AbstractRef):
      arg[...] = jnp.expand_dims(jax_core.freeze(squeezed_arg), dim)

  return [jnp.expand_dims(out, 0) for out in outs], (0,) * len(outs)

