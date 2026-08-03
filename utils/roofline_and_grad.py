from typing import Callable

def roofline_and_grad(
  f: Callable,
  mesh: Mesh | AbstractMesh,
  in_specs: Specs,
  out_specs: Specs,
  *,
  pin_lhs_in_vmem: bool = False,
  pin_rhs_in_vmem: bool = False,
  print_jaxpr: bool = False,
) -> Callable[..., tuple[ShapeDtypeStructTree, RooflineResult, RooflineResult]]:
  @util.wraps(f)
  @traceback_util.api_boundary
  def wrapped(*args):
    primal_shapes, fwd_result = roofline(
      f,
      mesh,
      in_specs,
      out_specs,
      pin_lhs_in_vmem=pin_lhs_in_vmem,
      pin_rhs_in_vmem=pin_rhs_in_vmem,
      print_jaxpr=print_jaxpr,
    )(*args)

    return (
      primal_shapes,
      fwd_result,
      roofline(
        f,
        mesh,
        in_specs,
        out_specs,
        pin_lhs_in_vmem=pin_lhs_in_vmem,
        pin_rhs_in_vmem=pin_rhs_in_vmem,
        vjp=True,
        print_jaxpr=print_jaxpr,
      )(
        *tree_map(
          lambda x: api.ShapeDtypeStruct(
            x.shape,
            jnp.int32 if x.dtype == jnp.int32 else jnp.bfloat16,
            sharding=x.sharding,
          ),
          args,
        )
      )[1],
    )

  return wrapped

