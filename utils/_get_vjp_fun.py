import itertools
from typing import Callable

def _get_vjp_fun(
    primal_fun: Callable,
    *,
    in_tree: tree_util.PyTreeDef,
    in_avals: Sequence[core.AbstractValue],
    out_avals: Sequence[core.AbstractValue],
    has_named_shardings: bool,
    in_shardings_hlo: tuple[HloSharding | None, ...],
    out_shardings_hlo: tuple[HloSharding | None, ...],
    in_named_shardings: tuple[NamedSharding | None, ...],
    out_named_shardings: tuple[NamedSharding | None, ...],
    device_assignment: Sequence[sharding_impls.Device] | None,
    apply_jit: bool,
    flat_primal_fun: bool = False,
    mesh: mesh_lib.AbstractMesh | None = None,
) -> tuple[Callable, Sequence[core.AbstractValue]]:
  # Since jax.vjp does not handle kwargs, it is easier to do all the work
  # here with flattened functions.
  # apply_jit=False is only used for backwards compatibility with the graph
  # graph serialization. When apply_jit=True, we must pass a device assignment.
  # flat_primal_fun=False is used only from jax2tf, and it means that the
  # `primal_fun` takes PyTree `*args` and `**kwargs`.
  def fun_vjp_jax(*args_and_out_cts_flat_jax):
    # Takes a flat list of primals and output cotangents
    def flattened_primal_fun_jax(*args_flat):
      args, kwargs = in_tree.unflatten(args_flat)
      res = primal_fun(*args, **kwargs)
      res_flat, _ = tree_util.tree_flatten(res)
      return res_flat

    args_flat_jax, out_cts_flat_jax = util.split_list(args_and_out_cts_flat_jax,
                                                      [len(in_avals)])
    _, pullback_jax = api.vjp(primal_fun if flat_primal_fun else flattened_primal_fun_jax,
                              *args_flat_jax)
    return pullback_jax(out_cts_flat_jax)

  vjp_in_avals = list(
      itertools.chain(in_avals,
                      map(lambda a: a.to_tangent_aval(), out_avals)))

  if apply_jit:
    if has_named_shardings or mesh:
      vjp_in_shardings = tuple(
          _get_named_sharding(has_named_shardings, named_sharding,
                              hlo_sharding, aval, mesh)  # pyrefly: ignore[bad-argument-type]
          for named_sharding, hlo_sharding, aval in zip(
            itertools.chain(in_named_shardings, out_named_shardings),
            itertools.chain(in_shardings_hlo, out_shardings_hlo),
            vjp_in_avals))
      vjp_out_shardings = tuple(
        _get_named_sharding(has_named_shardings, named_sharding,
                            hlo_sharding, aval, mesh)  # pyrefly: ignore[bad-argument-type]
        for named_sharding, hlo_sharding, aval in zip(
          in_named_shardings, in_shardings_hlo, in_avals))
    else:
      assert device_assignment is not None
      vjp_in_shardings = tuple(
          _hlo_sharding_to_gspmd_sharding(s, device_assignment)
          for s in itertools.chain(in_shardings_hlo, out_shardings_hlo))
      vjp_out_shardings = tuple(
          _hlo_sharding_to_gspmd_sharding(s, device_assignment)
          for s in in_shardings_hlo)
    return pjit.pjit(fun_vjp_jax,
                     in_shardings=vjp_in_shardings,
                     out_shardings=vjp_out_shardings), vjp_in_avals
  else:
    return fun_vjp_jax, vjp_in_avals

