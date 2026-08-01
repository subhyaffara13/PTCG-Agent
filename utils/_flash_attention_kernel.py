
def _flash_attention_kernel(q_tile_ref, *args, **kwargs):
  block_b = q_tile_ref.shape[0]
  # If we're not going to tile the softmax, then we can avoid a bunch of VPU ops.
  if kwargs["block_k"] == kwargs["kv_seq_len"]:
    kernel = _flash_attention_kernel_single_batch_single_step
  else:
    kernel = _flash_attention_kernel_single_batch
  for batch_idx in range(block_b):
    kernel((batch_idx, 0), q_tile_ref, *args, **kwargs)

