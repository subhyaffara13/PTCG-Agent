
def tpu_custom_call_batcher(axis_data, args, dims, **kwargs):
  if axis_data.size != 1:
    raise NotImplementedError(
        "tpu_custom_call does not support non-trivial batching."
    )
  unbatched_args = tuple(
      a if (d is None or d is None) else a[d]
      for a, d in zip(args, dims, strict=True)
  )
  out_unbatched = tpu_custom_call_p.bind(*unbatched_args, **kwargs)
  out = tuple(o[None] for o in out_unbatched)
  return out, (0,) * len(out)

