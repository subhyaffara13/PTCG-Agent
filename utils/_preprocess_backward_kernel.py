
def _preprocess_backward_kernel(out_ref, dout_ref, delta_ref, head_dim: int):
  # load
  head_mask = (jnp.arange(out_ref.shape[-1]) < head_dim)[None, :]
  o = plgpu.load(out_ref, mask=head_mask, other=0.0)
  do = plgpu.load(dout_ref, mask=head_mask, other=0.0)
  # compute
  delta = jnp.sum(o * do, axis=1)
  # write-back
  delta_ref[...] = delta.astype(delta_ref.dtype)

