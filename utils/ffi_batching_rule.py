from typing import Any

def ffi_batching_rule(
    prim,
    args,
    dims,
    *,
    vmap_method: str | None,
    result_avals: Sequence[core.ShapedArray],
    **kwargs: Any,
):
  from jax._src.lax import control_flow  # pyrefly: ignore[missing-import]
  from jax._src.lax import lax  # pyrefly: ignore[missing-import]

  axis_size, = {a.shape[d] for a, d in zip(args, dims)
                if d is not None}
  new_args = [arg if dim is None else
              batching.moveaxis(arg, dim, 0) for arg, dim in zip(args, dims)]
  batched_result_avals = tuple(
      core.unmapped_aval(axis_size, 0, aval) for aval in result_avals)

  # For FFI calls we must update the layouts. We handle the output layouts
  # here, but the input layout updates depend on the vmap_method parameter.
  if (
      vmap_method not in ("sequential", "sequential_unrolled") and
      kwargs.get("output_layouts") is not None
  ):
    kwargs["output_layouts"] = tuple(
        None if layout is None else tuple(n + 1 for n in layout) + (0,)
        for layout in kwargs["output_layouts"])

  if vmap_method == "legacy_vectorized":
    # This method is kept to support the behavior that was previously exposed
    # when using `vectorized=True`.
    if kwargs.get("input_layouts") is not None:
      kwargs["input_layouts"] = tuple(
          layout if d is None else
          (None if layout is None else tuple(n + 1 for n in layout) + (0,))
          for layout, d in zip(kwargs["input_layouts"], dims))
    outvals = prim.bind(
        *new_args,
        vmap_method=vmap_method,
        result_avals=batched_result_avals,
        **kwargs,
    )
  elif vmap_method == "expand_dims" or vmap_method == "broadcast_all":
    size = axis_size if vmap_method == "broadcast_all" else 1
    bcast_args = [
        lax.broadcast(x, (size,)) if d is None else x
        for x, d in zip(new_args, dims)]
    if kwargs.get("input_layouts") is not None:
      kwargs["input_layouts"] = tuple(
          None if layout is None else tuple(n + 1 for n in layout) + (0,)
          for layout in kwargs["input_layouts"])
    outvals = prim.bind(
      *bcast_args,
      vmap_method=vmap_method,
      result_avals=batched_result_avals,
      **kwargs,
    )
  elif vmap_method == "sequential" or vmap_method == "sequential_unrolled":
    is_batched = [d is not None for d in dims]
    unbatched_args, batched_args = util.partition_list(is_batched, new_args)
    def _batch_fun(batched_args):
      merged_args = util.merge_lists(is_batched, unbatched_args, batched_args)
      return prim.bind(
          *merged_args,
          result_avals=result_avals,
          vmap_method=vmap_method,
          **kwargs,
      )
    unroll = vmap_method == "sequential_unrolled"
    g = lambda _, x: ((), _batch_fun(x))
    _, outvals = control_flow.scan(g, (), batched_args, unroll=unroll)
  else:
    raise NotImplementedError(
        f"vmap is only supported for the {prim.name} primitive when vmap_method "
        "is one of 'sequential', 'sequential_unrolled', 'expand_dims', "
        f"'broadcast_all', or 'legacy_vectorized'. Got {vmap_method=}.")
  return tuple(outvals), (0,) * len(outvals)

