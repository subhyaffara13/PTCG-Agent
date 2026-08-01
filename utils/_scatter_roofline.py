
def _scatter_roofline(
    ctx: roofline.RooflineRuleContext,
    *args,
    **kw,
) -> roofline.RooflineResult:
  """Roofline for Jax's `scatter*` primitives.

  The `scatter` functionality itself is a simple data read and write, which
  contributes 0 flops.

  But, the jaxpr for each `scatter*` function (aside from `jax.lax.scatter`)
  contains an `update_jaxpr` that gets applied to the operand & scattered
  updates (e.g. `add` for `scatter_add`, or arbitrary unary function for
  `scatter_apply`), which *does* contribute flops. This `update_jaxpr` gets
  applied to every element of the scattered updates.

  Thus,
  flops = [# flops for `update_jaxpr` per element] * [# elements in `updates`].

  To calculate # flops for `update_jaxpr`, we convert the `update_jaxpr` back to
  a callable, and then call `roofline` on that callable. `update_jaxpr` does not
  contain any information about input shapes or dtypes; it expects scalars. It
  will therefore give us a # flops-per-element result, which we multiply by
  the size of the updates to get the total flops.
  """
  (_, indices, updates) = (
      roofline.RooflineShape.from_aval(aval) for aval in ctx.avals_in
  )

  update_jaxpr = kw.get('update_jaxpr')

  flops = 0
  if update_jaxpr:
    update_fn = lambda *inputs: core.eval_jaxpr(update_jaxpr, [], *inputs)
    # Create dummy scalar inputs.
    dummy_inputs = [
        api.ShapeDtypeStruct((), updates.dtype) for _ in update_jaxpr.invars
    ]
    # Calculate the flops for the `update_jaxpr` on scalar inputs.
    _, roofline_result = roofline.roofline(update_fn)(*dummy_inputs)
    # Multiply by the size of the updates to get the total flops.
    flops = roofline_result.unfused_flops * updates.size

  return roofline.RooflineResult(
      unfused_flops=flops,
      # Scatter accesses the equivalent of 3N update shapes (input, output, and
      # updates), and the scatter indices.
      unfused_hbm_bytes=(
          3 * updates.dtype.itemsize * updates.size
          + indices.dtype.itemsize * indices.size
      ),
  )

