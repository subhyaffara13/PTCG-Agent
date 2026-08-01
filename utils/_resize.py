
def _resize(a, new_shape, xp):
    # https://github.com/numpy/numpy/blob/v2.2.4/numpy/_core/fromnumeric.py#L1535
    a = xp.reshape(a, (-1,))

    new_size = 1
    for dim_length in new_shape:
        new_size *= dim_length
        if dim_length < 0:
            raise ValueError(
                'all elements of `new_shape` must be non-negative'
            )

    if xp_size(a) == 0 or new_size == 0:
        # First case must zero fill. The second would have repeats == 0.
        return xp.zeros_like(a, shape=new_shape)

    repeats = -(-new_size // xp_size(a))  # ceil division
    a = xp.concat((a,) * repeats)[:new_size]

    return xp.reshape(a, new_shape)


def _resize(image, shape: core.Shape, method: str | ResizeMethod,
            antialias: bool, precision):
  if len(shape) != image.ndim:
    msg = ('shape must have length equal to the number of dimensions of x; '
           f' {shape} vs {image.shape}')
    raise ValueError(msg)
  if isinstance(method, str):
    method = ResizeMethod.from_string(method)
  if method == ResizeMethod.NEAREST:
    return _resize_nearest(image, shape)
  assert isinstance(method, ResizeMethod)

  image, = promote_dtypes_inexact(image)
  # Skip dimensions that have scale=1 and translation=0, this is only possible
  # since all of the current resize methods (kernels) are interpolating, so the
  # output = input under an identity warp.
  spatial_dims = tuple(i for i in range(len(shape))
                       if not core.definitely_equal(image.shape[i], shape[i]))
  if method == ResizeMethod.CUBIC_PYTORCH and antialias:
    method = ResizeMethod.CUBIC
  radius, kernel = _kernels[method]
  scale = [1.0 if core.definitely_equal(shape[d], 0) else core.dimension_as_value(shape[d]) / core.dimension_as_value(image.shape[d])
           for d in spatial_dims]
  edge_padding = (method == ResizeMethod.CUBIC_PYTORCH and not antialias)
  return _scale_and_translate(image, shape, spatial_dims, scale,
                              [0.] * len(spatial_dims), kernel, antialias,
                              precision, edge_padding=edge_padding,
                              radius=radius)

