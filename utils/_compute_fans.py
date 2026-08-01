
def _compute_fans(shape: Sequence[int],
                  in_axis: int | Sequence[int] = -2,
                  out_axis: int | Sequence[int] = -1,
                  batch_axis: int | Sequence[int] = ()
                  ) -> tuple[float, float]:
  """
  Compute effective input and output sizes for a linear or convolutional layer.

  Axes not in in_axis, out_axis, or batch_axis are assumed to constitute the
  "receptive field" of a convolution (kernel spatial dimensions).
  """
  if isinstance(in_axis, int) and in_axis == -2 and len(shape) <= 1:
    raise ValueError(
        f"Can't compute input and output sizes of a {len(shape)}-dimensional"
        " weights tensor with default in_axis. Must be at least 2D or specify"
        " in_axis explicitly."
    )

  if isinstance(in_axis, int):
    in_size = shape[in_axis]
  else:
    in_size = math.prod([shape[i] for i in in_axis])
  if isinstance(out_axis, int):
    out_size = shape[out_axis]
  else:
    out_size = math.prod([shape[i] for i in out_axis])
  if isinstance(batch_axis, int):
    batch_size = shape[batch_axis]
  else:
    batch_size = math.prod([shape[i] for i in batch_axis])
  receptive_field_size = math.prod(shape) / in_size / out_size / batch_size
  fan_in = in_size * receptive_field_size
  fan_out = out_size * receptive_field_size
  return fan_in, fan_out

