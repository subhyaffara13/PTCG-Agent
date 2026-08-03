from typing import Optional
import math


def resize(
    image: np.ndarray,
    size: tuple[int, int],
    resample: Optional["PILImageResampling"] = None,
    reducing_gap: int | None = None,
    data_format: ChannelDimension | None = None,
    return_numpy: bool = True,
    input_data_format: str | ChannelDimension | None = None,
) -> np.ndarray:
    """
    Resizes `image` to `(height, width)` specified by `size` using the PIL library.

    Args:
        image (`np.ndarray`):
            The image to resize.
        size (`tuple[int, int]`):
            The size to use for resizing the image.
        resample (`int`, *optional*, defaults to `PILImageResampling.BILINEAR`):
            The filter to user for resampling.
        reducing_gap (`int`, *optional*):
            Apply optimization by resizing the image in two steps. The bigger `reducing_gap`, the closer the result to
            the fair resampling. See corresponding Pillow documentation for more details.
        data_format (`ChannelDimension`, *optional*):
            The channel dimension format of the output image. If unset, will use the inferred format from the input.
        return_numpy (`bool`, *optional*, defaults to `True`):
            Whether or not to return the resized image as a numpy array. If False a `PIL.Image.Image` object is
            returned.
        input_data_format (`ChannelDimension`, *optional*):
            The channel dimension format of the input image. If unset, will use the inferred format from the input.

    Returns:
        `np.ndarray`: The resized image.
    """
    requires_backends(resize, ["vision"])

    resample = resample if resample is not None else PILImageResampling.BILINEAR

    if not len(size) == 2:
        raise ValueError("size must have 2 elements")

    # For all transformations, we want to keep the same data format as the input image unless otherwise specified.
    # The resized image from PIL will always have channels last, so find the input format first.
    if input_data_format is None:
        input_data_format = infer_channel_dimension_format(image)
    data_format = input_data_format if data_format is None else data_format

    # To maintain backwards compatibility with the resizing done in previous image feature extractors, we use
    # the pillow library to resize the image and then convert back to numpy
    do_rescale = False
    if not isinstance(image, PIL.Image.Image):
        do_rescale = _rescale_for_pil_conversion(image)
        image = to_pil_image(image, do_rescale=do_rescale, input_data_format=input_data_format)
    height, width = size
    # PIL images are in the format (width, height)
    resized_image = image.resize((width, height), resample=resample, reducing_gap=reducing_gap)

    if return_numpy:
        resized_image = np.array(resized_image)
        # If the input image channel dimension was of size 1, then it is dropped when converting to a PIL image
        # so we need to add it back if necessary.
        resized_image = np.expand_dims(resized_image, axis=-1) if resized_image.ndim == 2 else resized_image
        # The image is always in channels last format after converting from a PIL image
        resized_image = to_channel_dimension_format(
            resized_image, data_format, input_channel_dim=ChannelDimension.LAST
        )
        # If an image was rescaled to be in the range [0, 255] before converting to a PIL image, then we need to
        # rescale it back to the original range.
        resized_image = rescale(resized_image, 1 / 255) if do_rescale else resized_image
    return resized_image


def resize(x, size, *, memory_format=None):
    assert isinstance(x, TensorBox)
    assert isinstance(size, (list, tuple))

    if memory_format is None:
        memory_format = torch.contiguous_format
    if memory_format == torch.preserve_format:
        raise RuntimeError(f"unsupported memory format: {memory_format}")

    if memory_format == torch.channels_last:
        assert len(size) == 4
    if memory_format == torch.channels_last_3d:
        assert len(size) == 5

    old_numel = x.get_numel()
    dtype = x.get_dtype()
    device = x.get_device_or_error()

    if (
        torch.are_deterministic_algorithms_enabled()
        and torch.utils.deterministic.fill_uninitialized_memory  # type: ignore[attr-defined]
    ):
        if is_float_dtype(dtype):
            uninitialized_val = float("nan")
        elif is_integer_dtype(dtype):
            uninitialized_val = torch.iinfo(dtype).max
        else:
            uninitialized_val = True
    else:
        # using zero as that is what empty does
        uninitialized_val = 0.0

    if V.graph.sizevars.statically_known_equals(old_numel, 0):  # type: ignore[arg-type]
        return full(size, uninitialized_val, dtype=dtype, device=device)

    strides = x.maybe_get_stride()
    has_overlapping = strides is not None and any(
        V.graph.sizevars.statically_known_equals(s, 0) for s in strides
    )
    if has_overlapping:
        # overlapping: provide a contiguous logical view
        x_flat = view(x, [old_numel])
    else:
        # non-overlapping: keep storage order
        if isinstance(x.data, ir.BaseView):
            x.data = x.data.unwrap_view()
        x_flat = as_strided(x, [old_numel], [1])
    flat_loader = x_flat.make_loader()
    out_stride = ir.FlexibleLayout.stride_ordered_for_memory_format(size, memory_format)
    out_indexer = ir.FixedLayout(device, dtype, size, out_stride).make_indexer()

    def inner_fn(idx):
        flat_index = out_indexer(idx)
        flat_index_expr = ops.index_expr(flat_index, torch.int64)
        limit = ops.index_expr(old_numel, torch.int64)
        mask = ops.lt(flat_index_expr, limit)
        return ops.masked(mask, lambda: flat_loader([flat_index]), uninitialized_val)

    out = Pointwise.create(
        device=device, dtype=dtype, inner_fn=inner_fn, ranges=list(size)
    )
    return out


def resize(a: ArrayLike, new_shape=None):
    # implementation vendored from
    # https://github.com/numpy/numpy/blob/v1.24.0/numpy/core/fromnumeric.py#L1420-L1497
    if new_shape is None:
        return a

    if isinstance(new_shape, int):
        new_shape = (new_shape,)

    a = a.flatten()

    new_size = 1
    for dim_length in new_shape:
        new_size *= dim_length
        if dim_length < 0:
            raise ValueError("all elements of `new_shape` must be non-negative")

    if a.numel() == 0 or new_size == 0:
        # First case must zero fill. The second would have repeats == 0.
        return torch.zeros(new_shape, dtype=a.dtype)

    repeats = -(-new_size // a.numel())  # ceil division
    a = concatenate((a,) * repeats)[:new_size]

    return reshape(a, new_shape)


def resize(scale, old_mats):
    new_mats = []
    for mat in old_mats:
        new_mats.append(zoom(mat, scale, order=0))
    return np.array(new_mats)


def resize(x, new_shape):
    """
    Return a new masked array with the specified size and shape.

    This is the masked equivalent of the `numpy.resize` function. The new
    array is filled with repeated copies of `x` (in the order that the
    data are stored in memory). If `x` is masked, the new array will be
    masked, and the new mask will be a repetition of the old one.

    See Also
    --------
    numpy.resize : Equivalent function in the top level NumPy module.

    Examples
    --------
    >>> import numpy as np
    >>> import numpy.ma as ma
    >>> a = ma.array([[1, 2] ,[3, 4]])
    >>> a[0, 1] = ma.masked
    >>> a
    masked_array(
      data=[[1, --],
            [3, 4]],
      mask=[[False,  True],
            [False, False]],
      fill_value=999999)
    >>> np.resize(a, (3, 3))
    masked_array(
      data=[[1, 2, 3],
            [4, 1, 2],
            [3, 4, 1]],
      mask=False,
      fill_value=999999)
    >>> ma.resize(a, (3, 3))
    masked_array(
      data=[[1, --, 3],
            [4, 1, --],
            [3, 4, 1]],
      mask=[[False,  True, False],
            [False, False,  True],
            [False, False, False]],
      fill_value=999999)

    A MaskedArray is always returned, regardless of the input type.

    >>> a = np.array([[1, 2] ,[3, 4]])
    >>> ma.resize(a, (3, 3))
    masked_array(
      data=[[1, 2, 3],
            [4, 1, 2],
            [3, 4, 1]],
      mask=False,
      fill_value=999999)

    """
    # We can't use _frommethods here, as N.resize is notoriously whiny.
    m = getmask(x)
    if m is not nomask:
        m = np.resize(m, new_shape)
    result = np.resize(x, new_shape).view(get_masked_subclass(x))
    if result.ndim:
        result._mask = m
    return result


def resize(a, new_shape):
    """
    Return a new array with the specified shape.

    If the new array is larger than the original array, then the new
    array is filled with repeated copies of `a`.  Note that this behavior
    is different from a.resize(new_shape) which fills with zeros instead
    of repeated copies of `a`.

    Parameters
    ----------
    a : array_like
        Array to be resized.

    new_shape : int or tuple of int
        Shape of resized array.

    Returns
    -------
    reshaped_array : ndarray
        The new array is formed from the data in the old array, repeated
        if necessary to fill out the required number of elements.  The
        data are repeated iterating over the array in C-order.

    See Also
    --------
    numpy.reshape : Reshape an array without changing the total size.
    numpy.pad : Enlarge and pad an array.
    numpy.repeat : Repeat elements of an array.
    ndarray.resize : resize an array in-place.

    Notes
    -----
    When the total size of the array does not change `~numpy.reshape` should
    be used.  In most other cases either indexing (to reduce the size)
    or padding (to increase the size) may be a more appropriate solution.

    Warning: This functionality does **not** consider axes separately,
    i.e. it does not apply interpolation/extrapolation.
    It fills the return array with the required number of elements, iterating
    over `a` in C-order, disregarding axes (and cycling back from the start if
    the new shape is larger).  This functionality is therefore not suitable to
    resize images, or data where each axis represents a separate and distinct
    entity.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[0,1],[2,3]])
    >>> np.resize(a,(2,3))
    array([[0, 1, 2],
           [3, 0, 1]])
    >>> np.resize(a,(1,4))
    array([[0, 1, 2, 3]])
    >>> np.resize(a,(2,4))
    array([[0, 1, 2, 3],
           [0, 1, 2, 3]])

    """
    if isinstance(new_shape, (int, nt.integer)):
        new_shape = (new_shape,)

    a = ravel(a)

    new_size = 1
    for dim_length in new_shape:
        new_size *= dim_length
        if dim_length < 0:
            raise ValueError(
                'all elements of `new_shape` must be non-negative'
            )

    if a.size == 0 or new_size == 0:
        # First case must zero fill. The second would have repeats == 0.
        return np.zeros_like(a, shape=new_shape)

    # ceiling division without negating new_size
    repeats = (new_size + a.size - 1) // a.size
    a = concatenate((a,) * repeats)[:new_size]

    return reshape(a, new_shape)


def resize(image, shape: core.Shape, method: str | ResizeMethod,
           antialias: bool = True,
           precision = lax.Precision.HIGHEST):
  """Image resize.

  The ``method`` argument expects one of the following resize methods:

  ``ResizeMethod.NEAREST``, ``"nearest"``
    `Nearest neighbor interpolation`_. The values of ``antialias`` and
    ``precision`` are ignored.

  ``ResizeMethod.LINEAR``, ``"linear"``, ``"bilinear"``, ``"trilinear"``, ``"triangle"``
    `Linear interpolation`_. If ``antialias`` is ``True``, uses a triangular
    filter when downsampling.

  ``ResizeMethod.CUBIC``, ``"cubic"``, ``"bicubic"``, ``"tricubic"``
    `Cubic interpolation`_, using the Keys cubic kernel.

  ``ResizeMethod.CUBIC_PYTORCH``, ``"cubic-pytorch"``, ``"bicubic-pytorch"``
    `Cubic interpolation`_, matching PyTorch's bicubic resizing behavior.
    Identical to ``ResizeMethod.CUBIC`` when antialiasing is enabled, but uses
    a different kernel and enables edge padding when antialiasing is disabled.

  ``ResizeMethod.LANCZOS3``, ``"lanczos3"``
    `Lanczos resampling`_, using a kernel of radius 3.

  ``ResizeMethod.LANCZOS5``, ``"lanczos5"``
    `Lanczos resampling`_, using a kernel of radius 5.

  ``ResizeMethod.AREA``, ``"area"``
    Area resampling. Computes the average of all pixels that fall within the
    output pixel's area. When downscaling, this acts as an anti-aliasing filter.
    When upscaling, it acts as a box filter, matching TensorFlow's behavior.

  .. _Nearest neighbor interpolation: https://en.wikipedia.org/wiki/Nearest-neighbor_interpolation
  .. _Linear interpolation: https://en.wikipedia.org/wiki/Bilinear_interpolation
  .. _Cubic interpolation: https://en.wikipedia.org/wiki/Bicubic_interpolation
  .. _Lanczos resampling: https://en.wikipedia.org/wiki/Lanczos_resampling

  This function does not support an ``align_corners`` argument like
  ``torch.nn.functional.interpolate``. That behavior can be emulated using
  :func:`scale_and_translate`.

  Args:
    image: a JAX array.
    shape: the output shape, as a sequence of integers with length equal to
      the number of dimensions of `image`. Note that :func:`resize` does not
      distinguish spatial dimensions from batch or channel dimensions, so this
      includes all dimensions of the image. To represent a batch or a channel
      dimension, simply leave that element of the shape unchanged.
    method: the resizing method to use; either a ``ResizeMethod`` instance or a
      string. Available methods are: LINEAR, LANCZOS3, LANCZOS5, CUBIC, CUBIC_PYTORCH.
    antialias: should an antialiasing filter be used when downsampling? Defaults
      to ``True``. Has no effect when upsampling.
  Returns:
    The resized image. The return type may differ from the input type depending
    on the ``method``. For ``ResizeMethod.NEAREST``, the return type is the same
    as the input type. For other methods, the output type will be promoted to a
    floating point type.
  """
  return _resize(image, core.canonicalize_shape(shape), method, antialias,
                 precision)


def resize(a: ArrayLike, new_shape: Shape) -> Array:
  """Return a new array with specified shape.

  JAX implementation of :func:`numpy.resize`.

  Args:
    a: input array or scalar.
    new_shape: int or tuple of ints. Specifies the shape of the resized array.

  Returns:
    A resized array with specified shape. The elements of ``a`` are repeated in
    the resized array, if the resized array is larger than the original array.

  See also:
    - :func:`jax.numpy.reshape`: Returns a reshaped copy of an array.
    - :func:`jax.numpy.repeat`: Constructs an array from repeated elements.

  Examples:
    >>> x = jnp.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> jnp.resize(x, (3, 3))
    Array([[1, 2, 3],
           [4, 5, 6],
           [7, 8, 9]], dtype=int32)
    >>> jnp.resize(x, (3, 4))
    Array([[1, 2, 3, 4],
           [5, 6, 7, 8],
           [9, 1, 2, 3]], dtype=int32)
    >>> jnp.resize(4, (3, 2))
    Array([[4, 4],
           [4, 4],
           [4, 4]], dtype=int32, weak_type=True)
  """
  util.check_arraylike("resize", a)
  new_shape = _ensure_index_tuple(new_shape)

  if any(dim_length < 0 for dim_length in new_shape):
    raise ValueError("all elements of `new_shape` must be non-negative")

  arr = ravel(a)

  new_size = math.prod(new_shape)
  if arr.size == 0 or new_size == 0:
    return array_creation.zeros_like(arr, shape=new_shape)

  repeats = ceil_of_ratio(new_size, arr.size)
  arr = tile(arr, repeats)[:new_size]

  return reshape(arr, new_shape)

