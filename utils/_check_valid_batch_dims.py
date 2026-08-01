
def _check_valid_batch_dims(bdims):
  for dim in bdims:
    if dim not in [0, None]:
      raise NotImplementedError(
        f"Currently only support batch_dim in [0, None], but got {dim=}")

