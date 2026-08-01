
def _device_put_batcher(batched_args, batch_dims, **params):
  mapped_batch_dims = [bd for bd in batch_dims if bd is not None]
  assert not mapped_batch_dims or all(
      mapped_batch_dims[0] == bd for bd in mapped_batch_dims[1:]
  ), batch_dims
  return device_put_p.bind(*batched_args, **params), batch_dims

