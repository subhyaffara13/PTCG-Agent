
def _tensor_to_numpy(tensor: torch.Tensor) -> np.ndarray:
  """Converts a tensor to a numpy array, safely handling 16-bit float dtypes."""
  if tensor.dtype == torch.bfloat16 or tensor.dtype == torch.float16:
    return tensor.float().numpy(force=True)
  return tensor.numpy(force=True)

