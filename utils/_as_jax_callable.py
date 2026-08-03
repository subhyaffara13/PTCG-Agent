from typing import Any, Callable

def _as_jax_callable(
    config: CustomCallBackendConfig,
    has_side_effects: TpuSideEffectType,
    out_type: Any,
    *,
    kernel_name: str | None,
    input_output_aliases: tuple[tuple[int, int], ...],
    metadata: Any | None,
) -> Callable[..., Any]:
  unpack = False
  if not isinstance(out_type, collections.abc.Iterable):
    out_type = (out_type,)
    unpack = True
  out_avals = tuple(ty if isinstance(ty, core.ShapedArray) else
                    core.typeof(ty) for ty in out_type)

  # We use jax.jit to make sure we hit the fast compilation cache.
  def apply_kernel(*args):
    result = tpu_custom_call_p.bind(
        *args,
        config=config,
        has_side_effects=has_side_effects,
        kernel_name=kernel_name,
        out_avals=out_avals,
        input_output_aliases=input_output_aliases,
        metadata=metadata,
    )
    return result[0] if unpack else result

  return api.jit(apply_kernel)

