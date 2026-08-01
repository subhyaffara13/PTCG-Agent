
def from_dlpack(
    ext_tensor: Any,
    *,
    device: _Device | None = None,
    copy: bool | None = None
) -> 'torch.Tensor':
    """from_dlpack(ext_tensor) -> Tensor

    Converts a tensor from an external library into a ``torch.Tensor``.

    The returned PyTorch tensor will share the memory with the input tensor
    (which may have come from another library). Note that in-place operations
    will therefore also affect the data of the input tensor. This may lead to
    unexpected issues (e.g., other libraries may have read-only flags or
    immutable data structures), so the user should only do this if they know
    for sure that this is fine.

    Args:
        ext_tensor (object with ``__dlpack__`` attribute, or a DLPack capsule):
            The tensor or DLPack capsule to convert.

            If ``ext_tensor`` is a tensor (or ndarray) object, it must support
            the ``__dlpack__`` protocol (i.e., have a ``ext_tensor.__dlpack__``
            method). Otherwise ``ext_tensor`` may be a DLPack capsule, which is
            an opaque ``PyCapsule`` instance, typically produced by a
            ``to_dlpack`` function or method.

        device (torch.device or str or None): An optional PyTorch device
            specifying where to place the new tensor. If None (default), the
            new tensor will be on the same device as ``ext_tensor``.

        copy (bool or None): An optional boolean indicating whether or not to copy
            ``self``. If None, PyTorch will copy only if necessary.

    Examples::

        >>> import torch.utils.dlpack
        >>> t = torch.arange(4)

        # Convert a tensor directly (supported in PyTorch >= 1.10)
        >>> t2 = torch.from_dlpack(t)
        >>> t2[:2] = -1  # show that memory is shared
        >>> t2
        tensor([-1, -1,  2,  3])
        >>> t
        tensor([-1, -1,  2,  3])

        # The old-style DLPack usage, with an intermediate capsule object
        >>> capsule = torch.utils.dlpack.to_dlpack(t)
        >>> capsule
        <capsule object "dltensor" at ...>
        >>> t3 = torch.from_dlpack(capsule)
        >>> t3
        tensor([-1, -1,  2,  3])
        >>> t3[0] = -9  # now we're sharing memory between 3 tensors
        >>> t3
        tensor([-9, -1,  2,  3])
        >>> t2
        tensor([-9, -1,  2,  3])
        >>> t
        tensor([-9, -1,  2,  3])

    """

    if hasattr(ext_tensor, '__dlpack__'):
        # Only populate kwargs if any of the optional arguments are, in fact, not None. Otherwise,
        # leave them out, since we might end up falling back to no-extra-kwargs __dlpack__ call.
        kwargs: dict[str, Any] = {}
        kwargs["max_version"] = (1, 0)

        # Track copy request for potential manual handling
        requested_copy = copy
        producer_handled_copy = True
        cross_device_transfer = False  # Will be set to True if device transfer is needed

        if copy is not None:
            kwargs["copy"] = copy

        # Parse the device parameter.
        # At this moment, it can either be a torch.device or a str representing
        # a torch.device, e.g. "cpu", "cuda", etc.
        # Get source device first (we need it to detect cross-device transfers)
        ext_device = ext_tensor.__dlpack_device__()

        if device is not None:
            if isinstance(device, str):
                device = torch.device(device)
            if not isinstance(device, torch.device):
                raise AssertionError(f"from_dlpack: unsupported device type: {type(device)}")

            # Convert target device to DLPack format
            target_dl_device = torch._C._torchDeviceToDLDevice(device)

            # Detect cross-device transfer by comparing source and target devices
            # E.g. CPU->CUDA, cuda:0->cuda:1, etc.
            cross_device_transfer = (ext_device != target_dl_device)

            # Only pass dl_device to producer if NOT cross-device transfer
            if not cross_device_transfer:
                kwargs["dl_device"] = target_dl_device

            # Cross-device transfer always requires a copy
            if cross_device_transfer and copy is False:
                raise ValueError(
                    f"cannot move DLPack tensor from device {ext_device} to {target_dl_device} "
                    "without copying. Set copy=None or copy=True."
                )

        # ext_device is either CUDA or ROCm, we need to pass the current
        # stream
        if ext_device[0] in (DLDeviceType.kDLCUDA, DLDeviceType.kDLROCM):
            stream = torch.cuda.current_stream(f'cuda:{ext_device[1]}')
            # cuda_stream is the pointer to the stream and it is a public
            # attribute, but it is not documented
            # The array API specify that the default legacy stream must be passed
            # with a value of 1 for CUDA
            # https://data-apis.org/array-api/latest/API_specification/array_object.html?dlpack-self-stream-none#dlpack-self-stream-none
            is_cuda = ext_device[0] == DLDeviceType.kDLCUDA
            # Since pytorch is not using PTDS by default, lets directly pass
            # the legacy stream
            stream_ptr = 1 if is_cuda and stream.cuda_stream == 0 else stream.cuda_stream
            kwargs["stream"] = stream_ptr

        # Try different parameter combinations until one works
        dlpack = None

        # Attempt 1: Try with all the parameters
        try:
            dlpack = ext_tensor.__dlpack__(**kwargs)
        except TypeError:
            pass

        # Attempt 2: Remove max_version
        if dlpack is None:
            kwargs.pop("max_version", None)
            try:
                dlpack = ext_tensor.__dlpack__(**kwargs)
            except TypeError:
                pass

        # Attempt 3: Remove copy
        if dlpack is None:
            kwargs.pop("copy", None)
            producer_handled_copy = False
            try:
                dlpack = ext_tensor.__dlpack__(**kwargs)
            except TypeError:
                pass

        # Attempt 4: Remove dl_device
        if dlpack is None:
            kwargs.pop("dl_device", None)
            dlpack = ext_tensor.__dlpack__(**kwargs)

        tensor = torch._C._from_dlpack(dlpack)

        # Manual copy if producer didn't handle it (cross-device already copies via .to())
        if requested_copy is True and not producer_handled_copy and not cross_device_transfer:
            tensor = tensor.clone()

        # Handle cross-device transfer by moving tensor to target device
        if cross_device_transfer:
            tensor = tensor.to(device)

        return tensor

    else:
        if device is not None or copy is not None:
            raise AssertionError(
                "device and copy kwargs not supported when ext_tensor is already a DLPack capsule."
            )
        # Old versions just call the converter
        dlpack = ext_tensor
        return torch._C._from_dlpack(dlpack)


def from_dlpack(x, /):
    t = torch.from_dlpack(x)
    return ndarray(t)


def from_dlpack(external_array,
                device: _jax.Device | Sharding | None = None,
                copy: bool | None = None):
  """Returns a :class:`~jax.Array` representation of a DLPack tensor.

  The returned :class:`~jax.Array` shares memory with ``external_array`` if no
  device transfer or copy was requested.

  Args:
    external_array: An array object that has ``__dlpack__`` and
      ``__dlpack_device__`` methods.
    device: The (optional) :py:class:`Device`, representing the device on which
      the returned array should be placed. If given, then the result is
      committed to the device. If unspecified, the resulting array will be
      unpacked onto the same device it originated from. Setting ``device`` to a
      device different from the source of ``external_array`` will require a
      copy, meaning ``copy`` must be set to either ``True`` or ``None``.
    copy: An (optional) boolean, controlling whether or not a copy is performed.
      If ``copy=True`` then a copy is always performed, even if unpacked onto
      the same device. If ``copy=False`` then the copy is never performed and
      will raise an error if necessary. When ``copy=None`` then a copy may be
      performed if needed for a device transfer.

  Returns:
    A jax.Array

  Note:
    While JAX arrays are always immutable, dlpack buffers cannot be marked as
    immutable, and it is possible for processes external to JAX to mutate them
    in-place. If a jax Array is constructed from a dlpack buffer and the buffer
    is later modified in-place, it may lead to undefined behavior when using
    the associated JAX array.
  """
  if isinstance(device, Sharding):
    device_set = device.device_set
    if len(device_set) > 1:
      raise ValueError(
        "from_dlpack can only unpack a dlpack tensor onto a singular device, but "
        f"a Sharding with {len(device_set)} devices was provided."
      )
    device, = device_set
  if not hasattr(external_array, "__dlpack__") or not hasattr(external_array, "__dlpack_device__"):
    raise TypeError(
        "The array passed to from_dlpack must have __dlpack__ and __dlpack_device__ methods."
    )

  dl_device_type, device_id = external_array.__dlpack_device__()
  try:
    dl_device_platform = _DL_DEVICE_TO_PLATFORM[dl_device_type]
  except KeyError:
    raise TypeError(
        "Array passed to from_dlpack is on unsupported device type "
        f"(DLDeviceType: {dl_device_type}, array: {external_array}"
    ) from None

  backend = xla_bridge.get_backend(dl_device_platform)
  dlpack_device = backend.device_from_local_hardware_id(device_id)
  _check_device(device, dlpack_device, copy)
  if _is_tensorflow_tensor(external_array):
    # TensorFlow does not support stream=.
    stream = None
  elif dl_device_type == DLDeviceType.kDLCUDAHost:
    # Some producers (e.g. torch.Tensor with is_pinned()) route pinned tensors
    # through their CPU __dlpack__, which rejects a non-None stream argument.
    stream = None
  else:
    try:
      stream = dlpack_device.get_stream_for_external_ready_events()
    except _jax.JaxRuntimeError as err:
      if "UNIMPLEMENTED" in str(err):
        stream = None
      else:
        raise
  dlpack = external_array.__dlpack__(stream=stream)

  try:
    if jaxlib_extension_version >= 467:
      arr = _jax.dlpack_managed_tensor_to_buffer(
        dlpack, dlpack_device, stream, copy, int(dl_device_type))
    else:
      arr = _jax.dlpack_managed_tensor_to_buffer(
        dlpack, dlpack_device, stream, copy)
  except xla_client.XlaRuntimeError as e:
    se = str(e)
    if "is not aligned to" in se:
      i = se.index("is not aligned to")
      raise ValueError(
        "Specified input which requires a copy since the source data "
        f"buffer {se[i:]} However copy=False. Set copy=True or "
        "copy=None to perform the requested operation."
      )
    else:
      raise
  # TODO(phawkins): when we are ready to support x64 arrays in
  # non-x64 mode, change the semantics to not canonicalize here.
  arr = jnp.asarray(arr, dtype=dtypes.canonicalize_dtype(arr.dtype))
  if copy:
    # copy was already handled by dlpack_managed_tensor_to_buffer.
    copy = None
  return _place_array(arr, device, dlpack_device, copy)


def from_dlpack(x: Any, /, *, device: xc.Device | Sharding | None = None,
                copy: bool | None = None) -> Array:
  """Construct a JAX array via DLPack.

  JAX implementation of :func:`numpy.from_dlpack`.

  Args:
    x: An object that implements the DLPack_ protocol via the ``__dlpack__``
      and ``__dlpack_device__`` methods, or a legacy DLPack tensor on either
      CPU or GPU.
    device: An optional :class:`~jax.Device` or :class:`~jax.sharding.Sharding`,
      representing the single device onto which the returned array should be placed.
      If given, then the result is committed to the device. If unspecified,
      the resulting array will be unpacked onto the same device it originated from.
      Setting ``device`` to a device different from the source of ``external_array``
      will require a copy, meaning ``copy`` must be set to either ``True`` or ``None``.
    copy: An optional boolean, controlling whether or not a copy is performed.
      If ``copy=True`` then a copy is always performed, even if unpacked onto the
      same device. If ``copy=False`` then the copy is never performed and will raise
      an error if necessary. When ``copy=None`` (default) then a copy may be performed
      if needed for a device transfer.

  Returns:
    A JAX array of the input buffer.

  Note:
    While JAX arrays are always immutable, dlpack buffers cannot be marked as
    immutable, and it is possible for processes external to JAX to mutate them
    in-place. If a JAX Array is constructed from a dlpack buffer without copying
    and the source buffer is later modified in-place, it may lead to undefined
    behavior when using the associated JAX array.

  Examples:
    Passing data between NumPy and JAX via DLPack_:

    >>> import numpy as np
    >>> rng = np.random.default_rng(42)
    >>> x_numpy = rng.random(4, dtype='float32')
    >>> print(x_numpy)
    [0.08925092 0.773956   0.6545715  0.43887842]
    >>> hasattr(x_numpy, "__dlpack__")  # NumPy supports the DLPack interface
    True

    >>> import jax.numpy as jnp
    >>> x_jax = jnp.from_dlpack(x_numpy)
    >>> print(x_jax)
    [0.08925092 0.773956   0.6545715  0.43887842]
    >>> hasattr(x_jax, "__dlpack__")  # JAX supports the DLPack interface
    True

    >>> x_numpy_round_trip = np.from_dlpack(x_jax)
    >>> print(x_numpy_round_trip)
    [0.08925092 0.773956   0.6545715  0.43887842]

  .. _DLPack: https://dmlc.github.io/dlpack
  """
  from jax.dlpack import from_dlpack
  return from_dlpack(x, device=device, copy=copy)

