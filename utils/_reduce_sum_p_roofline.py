
def _reduce_sum_p_roofline(
    ctx: roofline.RooflineRuleContext,
    *args,
    axes: tuple[int, ...],
    **kw,
) -> roofline.RooflineResult:
  (x,) = (roofline.RooflineShape.from_aval(aval) for aval in ctx.avals_in)
  domain_size = np.prod([x.shape[i] for i in axes])
  other_axes = set(range(len(x.shape))) - set(axes)
  result_size = np.prod([x.shape[i] for i in other_axes])

  return roofline.RooflineResult(
      # To add n values, we do n - 1 add operations, and we have to do that
      # for every element in the result.
      unfused_flops=int((domain_size - 1) * result_size),
      # Size of input, plus output. (We assume that the output is also used
      # as accumulator.)
      unfused_hbm_bytes=int(x.dtype.itemsize * (x.size + result_size)),
  )

