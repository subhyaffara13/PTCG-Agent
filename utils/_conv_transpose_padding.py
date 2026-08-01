
def _conv_transpose_padding(k, s, padding):
  """Calculate before and after padding for a dim of transposed convolution.

  Args:
    k: int: kernel dimension.
    s: int: dimension stride value.
    padding: tuple of ints or 'same' or 'valid' padding mode for original forward conv.

  Returns:
    2-tuple: ints: before and after padding for transposed convolution.
  """
  if padding == 'SAME':
    pad_len = k + s - 2
    if s > k - 1:
      pad_a = k - 1
    else:
      pad_a = int(np.ceil(pad_len / 2))
  elif padding == 'VALID':
    pad_len = k + s - 2 + max(k - s, 0)
    pad_a = k - 1
  elif isinstance(padding, tuple):
    pads = tuple(k - p - 1 for p in padding)
    pad_a = pads[0]
    pad_len = sum(pads)
  else:
    raise ValueError(f"Invalid padding mode: {padding}")
  pad_b = pad_len - pad_a
  return pad_a, pad_b

