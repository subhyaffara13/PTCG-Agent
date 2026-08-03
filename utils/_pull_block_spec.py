from typing import Any, Callable

def _pull_block_spec(
    jaxpr: core.Jaxpr,
    out_block_specs: tuple[pallas_core.BlockSpec, ...],
    *,
    read_usage_env: Callable[[core.Var], set[Usage]],
    scalar_prefetch_handler: Any | None = None,
    grid_len: int,
    strict_mode: bool = True,
) -> tuple[
    tuple[pallas_core.BlockSpec | pallas_core.NoBlockSpec, ...],
    tuple[dict[core.Var, pallas_core.BlockSpec], dict[int, Any]],
]:
  # initialize block transforms to identity for each output
  out_block_transforms = _init_block_transforms(out_block_specs)

  in_block_transforms, (env, scalar_prefetch_fn_env) = _pull_block_transform(
      jaxpr,
      out_block_transforms,
      read_usage_env=read_usage_env,
      scalar_prefetch_handler=scalar_prefetch_handler,
      grid_len=grid_len,
      strict_mode=strict_mode,
  )

  # apply accumulated block transforms to get final block specs
  env = {v: _apply_block_transform(out_block_specs, bt)
         for v, bt in env.items()}
  env = cast(dict[core.Var, pallas_core.BlockSpec], env)
  in_block_specs = tuple(_apply_block_transform(out_block_specs, bt)
                         for bt in in_block_transforms)

  return (
      in_block_specs,
      (env, scalar_prefetch_fn_env),
  )

