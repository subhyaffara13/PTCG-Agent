
def _slice_transpose_fancy(out_ct, operand, *, start_indices, limit_indices, strides):
  assert isinstance(operand, ad.GradAccum)
  if type(out_ct) is ad_util.Zero or isinstance(operand, ad.NullAccum):
    return
  if isinstance(operand, ad.RefAccum):
    slices = map(_slice, start_indices, limit_indices, strides)
    assert operand.ref is not None
    operand.ref.addupdate(out_ct, tuple(slices))
  else:
    operand_aval, = lax_utils.ensure_shaped(operand.aval)
    if strides is None or np.all(np.equal(strides, 1)):
      pads = zip(start_indices, np.subtract(operand_aval.shape, limit_indices),
                 (0,) * len(start_indices))
    else:
      real_limits = np.add(
        start_indices,
        np.where(np.array(out_ct.shape) == 0, 0,
                 np.add(1, np.multiply(np.subtract(out_ct.shape, 1), strides))))
      pads = zip(start_indices, np.subtract(operand_aval.shape, real_limits),
                 np.subtract(strides, 1))
    operand.accum(lax.pad(out_ct, lax._const(out_ct, 0), pads))

