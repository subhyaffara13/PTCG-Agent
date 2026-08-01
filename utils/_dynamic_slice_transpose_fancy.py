
def _dynamic_slice_transpose_fancy(out_ct, operand, *start_indices, slice_sizes):
  assert isinstance(operand, ad.GradAccum)
  assert all(not isinstance(s, ad.GradAccum) for s in start_indices)
  if type(out_ct) is ad_util.Zero or isinstance(operand, ad.NullAccum):
    return
  if isinstance(operand, ad.RefAccum):
    assert operand.ref is not None
    operand.ref.addupdate(out_ct, tuple(map(ds, start_indices, slice_sizes)))
  else:
    operand_aval, = lax_utils.ensure_shaped(operand.aval)
    zeros = lax.full(operand_aval.shape, 0, operand_aval.dtype,
                     sharding=operand_aval.sharding)
    zeros = core.pvary(zeros, tuple(operand_aval.mat.varying))
    operand.accum(dynamic_update_slice_p.bind(zeros, out_ct, *start_indices))

