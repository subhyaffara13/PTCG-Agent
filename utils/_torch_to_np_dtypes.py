
def _torch_to_np_dtypes() -> dict[torch_.dtype, _NpDType]:
  """Returns mapping torch -> numpy dtypes."""
  torch = lazy.torch
  return {
      torch.bool: np.bool_,
      torch.uint8: np.uint8,
      torch.int8: np.int8,
      torch.int16: np.int16,
      torch.int32: np.int32,
      torch.int64: np.int64,
      # TODO(epot): torch.bfloat:
      torch.float16: np.float16,
      torch.float32: np.float32,
      torch.float64: np.float64,
      torch.complex64: np.complex64,
      torch.complex128: np.complex128,
  }

