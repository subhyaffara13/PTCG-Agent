from typing import Any, Callable

def _uses_arguments(
    index_map: Callable[..., Any], num_args: int
) -> Sequence[bool]:
  if not num_args:
    return ()

  jaxpr, _, _ = pe.trace_to_jaxpr_dynamic(
      lu.wrap_init(
          index_map,
          debug_info=api_util.debug_info("pallas index_map",
                                         index_map,
                                         (0,) * num_args, {})),
      (core.ShapedArray((), jnp.int32),) * num_args
  )
  _, used_inputs = pe.dce_jaxpr(jaxpr, used_outputs=[True] * len(jaxpr.outvars))
  return used_inputs

