import copy
from typing import Any

def to_dlpack(x: Array, stream: int | Any | None = None,
              src_device: _jax.Device | None = None,
              dl_device: tuple[DLDeviceType, int] | None = None,
              max_version: tuple[int, int] | None = None,
              copy : bool | None = None):
  """Returns a DLPack tensor that encapsulates a :class:`~jax.Array` ``x``.

  Args:
    x: a :class:`~jax.Array`, on either CPU or GPU.
    stream: optional platform-dependent stream to wait on until the buffer is
      ready. This corresponds to the `stream` argument to ``__dlpack__``
      documented in https://dmlc.github.io/dlpack/latest/python_spec.html.
    src_device: either a CPU or GPU :class:`~jax.Device`.
    dl_device: a tuple of ``(dl_device_type, local_hardware_id)`` in DLPack
      format e.g. as produced by ``__dlpack_device__``.
    max_version: the maximum DLPack version that the consumer (i.e. caller of
      ``__dlpack__``) supports in the form of a 2-tuple of ``(major, minor)``.
      This function is not guaranteed to return a capsule of version
      ``max_version``.
    copy: a boolean indicating whether or not to copy the input. If
      ``copy=True`` then the function must always copy. When
      ``copy=False`` then the function must never copy, and must raise an error
      when a copy is deemed necessary. If ``copy=None`` then the function must
      avoid a copy if possible but may copy if needed.

  Returns:
    A DLPack PyCapsule object.

  Note:
    While JAX arrays are always immutable, ``DLPackManagedTensor`` buffers
    cannot be marked as immutable, and it is possible for processes external
    to JAX to mutate them in-place. If a DLPack buffer derived from a JAX array
    is mutated, it may lead to undefined behavior when using the associated JAX
    array. When JAX eventually supports ``DLManagedTensorVersioned``
    (DLPack 1.0), it will be possible to specify that a buffer is read-only.
  """
  if not isinstance(x, array.ArrayImpl):
    raise TypeError("Argument to to_dlpack must be a jax.Array, "
                    f"got {type(x)}")

  device = None
  dl_device_type, local_hardware_id = dl_device if dl_device else (None, None)
  if dl_device_type:
    try:
      dl_device_platform = _DL_DEVICE_TO_PLATFORM[dl_device_type]
      backend = xla_bridge.get_backend(dl_device_platform)
      device = backend.device_from_local_hardware_id(local_hardware_id)
    except KeyError:
      # https://data-apis.org/array-api/latest/API_specification/generated/array_api.array.__dlpack__.html
      # recommends using BufferError.
      raise BufferError(
          "The device specification passed to to_dlpack contains an"
          f" unsupported device type (DLDeviceType: {dl_device_type})"
      ) from None

  # As new versions are adopted over time, we can maintain some legacy paths
  # for compatibility mediated through the max_version parameter.
  # TODO(micky774): Deprecate default usage of DLPackManagedTensor when XLA
  # supports DLManagedTensorVersioned (DLPack version 1.0) and repurpose the
  # current _to_dlpack as a legacy path for (0,5) <= max_version < (1,0).
  if max_version is None or max_version >= DLPACK_VERSION:
    # Latest
    return _to_dlpack(
      x, stream=stream,
      src_device=src_device,
      device=device,
      copy=copy
    )
  elif max_version >= MIN_DLPACK_VERSION:
    # Oldest supported
    return _to_dlpack(
      x, stream=stream,
      src_device=src_device,
      device=device,
      copy=copy
    )
  else:
    raise BufferError(
      f"JAX does not support any version below {MIN_DLPACK_VERSION} but "
      f"version ({max_version}) was requested."
    )

