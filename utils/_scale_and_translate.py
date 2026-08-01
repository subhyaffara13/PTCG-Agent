
def _scale_and_translate(x, output_shape: core.Shape,
                         spatial_dims: Sequence[int], scale, translation,
                         kernel, antialias: bool, precision,
                         edge_padding: bool = False, radius: int | None = None):
  """
  Args:
    edge_padding: if False, pixels that are off the edge of the input
      image will receive zero weight. If True, the edges of the input image are
      repeated.
    radius: the radius of the kernel. May be None if edge_padding is False.
  """
  input_shape = x.shape
  assert len(input_shape) == len(output_shape)
  assert len(spatial_dims) == len(scale)
  assert len(spatial_dims) == len(translation)
  if len(spatial_dims) == 0:
    return x
  contractions = []
  in_indices = list(range(len(output_shape)))
  out_indices = list(range(len(output_shape)))
  for i, d in enumerate(spatial_dims):
    d = canonicalize_axis(d, x.ndim)
    m = input_shape[d]
    n = output_shape[d]
    w = compute_weight_mat(
        m, n, scale[i], translation[i], kernel, antialias,
        edge_padding=edge_padding, radius=radius,
    ).astype(x.dtype)
    contractions.append(w)
    contractions.append([d, len(output_shape) + i])
    out_indices[d] = len(output_shape) + i
  contractions.append(out_indices)
  return jnp_einsum.einsum(x, in_indices, *contractions, precision=precision)

