from typing import Callable

def _trace_kernel_to_jaxpr(
    fun: Callable,
    debug_info: jax_core.DebugInfo,
    grid_mapping: GridMapping,
    kernel_avals: tuple[state.AbstractRef, ...],
    kernel_in_tree: tree_util.PyTreeDef,
    kernel_in_transforms: tuple[tuple[state.Transform, ...], ...],
    indexer: bool = False,
) -> tuple[jax_core.Jaxpr, tuple[jax_typing.Array, ...]]:
  wrapped_kernel_fun, out_tree_thunk = api_util.flatten_fun(
      lu.wrap_init(fun, debug_info=debug_info), kernel_in_tree)
  wrapped_kernel_fun = primitives.wrap_with_transforms(
      wrapped_kernel_fun, kernel_in_transforms
  )
  with grid_mapping.trace_env(), config._check_vma(False):
    with config.mutable_array_checks(False):
      jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(
          wrapped_kernel_fun, kernel_avals
      )
      jaxpr, _ = pe.dce_jaxpr(jaxpr, used_outputs=[True] * len(jaxpr.outvars),
                              instantiate=True)
    if consts:
      consts_avals = [
          aval
          for c in consts
          if not isinstance(aval := jax_core.typeof(c), state.AbstractRef)
      ]
      if consts_avals:
        ctx = jax_core.JaxprPpContext()
        pp_consts_avals = ", ".join(
            jax_core.pp_aval(aval, ctx) for aval in consts_avals
        )
        raise ValueError(
            "The kernel function in the pallas_call"
            f" {debug_info.func_src_info} captures constants"
            f" [{pp_consts_avals}]. You should pass them as inputs."
        )

  kernel_out_tree = out_tree_thunk()
  if not indexer and kernel_out_tree != tree_util.tree_structure(None):
    raise ValueError(
        f"The kernel function in the pallas_call {debug_info.func_src_info} "
        f"should return None. It returns a PyTree: {kernel_out_tree}")
  return jaxpr, tuple(consts)

