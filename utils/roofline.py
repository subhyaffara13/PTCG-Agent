from typing import Callable

def roofline(
    f: Callable,
    mesh: Mesh | AbstractMesh | None = None,
    in_specs: Specs | None = None,
    out_specs: Specs | None = None,
    *,
    pin_lhs_in_vmem: bool = False,
    pin_rhs_in_vmem: bool = False,
    vjp: bool = False,
    print_jaxpr: bool = False,
) -> Callable[..., tuple[ShapeDtypeStructTree, RooflineResult]]:
  @util.wraps(f)
  @traceback_util.api_boundary
  def wrapped(*args):
    wrapped_f = f
    if in_specs is not None and out_specs is not None and mesh is not None:
      wrapped_f = shard_map(wrapped_f, mesh=mesh, in_specs=in_specs,
                            out_specs=out_specs)
    if vjp:
      wrapped_f = _f_with_vjp(wrapped_f)

    jaxpr, out_shapes = make_jaxpr(wrapped_f, return_shape=True)(*args)

    def make_sharded_shape_dtype_struct(
      shape: api.ShapeDtypeStruct, out_spec: Specs
    ) -> api.ShapeDtypeStruct:
      assert mesh is not None
      return api.ShapeDtypeStruct(
        shape.shape, shape.dtype, sharding=NamedSharding(mesh, out_spec)
      )

    if out_specs is not None and mesh is not None:
      out_specs_flat = broadcast_prefix(out_specs, out_shapes)
      flat_out_shapes, treedef = tree_flatten(out_shapes)
      flat_out_shapes = map(
          make_sharded_shape_dtype_struct, flat_out_shapes, out_specs_flat
      )
      out_shapes = tree_unflatten(treedef, flat_out_shapes)

    used_outputs = (True,) * len(jaxpr.jaxpr.outvars)
    jaxpr, _ = dce_jaxpr(jaxpr.jaxpr, used_outputs)
    shard_map_eqns = [
        e for e in jaxpr.eqns if e.primitive == shard_map_p
    ]
    if shard_map_eqns:
      try:
        jaxpr = shard_map_eqns[-1].params["jaxpr"]
      except KeyError:
        raise ValueError(f"Missing shard_map jaxpr in {jaxpr}.")

    if print_jaxpr:
      print(jaxpr)

    return out_shapes, _roofline_interpreter(
        util.fun_qual_name(f),
        jaxpr,
        mesh,
        pin_lhs_in_vmem=pin_lhs_in_vmem,
        pin_rhs_in_vmem=pin_rhs_in_vmem,
    )

  return wrapped

