
def devices(xp):
    """Fixture that returns a list of all devices for the backend, plus None.
    Used to test input->output device propagation.

    Usage
    -----
    from scipy._lib._array_api import xp_device

    def test_device(xp, devices):
        for d in devices:
            x = xp.asarray(..., device=d)
            y = f(x)
            assert xp_device(y) == xp_device(x)
    """
    if is_cupy(xp):
        # CuPy does not support devices other than the current one
        # data-apis/array-api-compat#293
        pytest.xfail(reason="data-apis/array-api-compat#293")
    if is_dask(xp):
        # Skip dummy DASK_DEVICE from array-api-compat, which does not propagate
        return ["cpu", None]
    if is_jax(xp):
        # The .device attribute is not accessible inside jax.jit; the consequence
        # (downstream of array-api-compat hacks) is that a non-default device in
        # input is not guaranteed to propagate to the output even if the scipy code
        # states `device=xp_device(arg)`` in all array creation functions.
        # While this issue is specific to jax.jit, it would be unnecessarily
        # verbose to skip the test for each jit-capable function and run it for
        # those that only support eager mode.
        pytest.xfail(reason="jax-ml/jax#26000")
    if is_torch(xp):
        devices = xp.__array_namespace_info__().devices()
        # open an issue about this - cannot branch based on `any`/`all`?
        return (device for device in devices if device.type != 'meta')
    return tuple(xp.__array_namespace_info__().devices()) + (None,)


def devices(
    backend: str | xla_client.Client | None = None
) -> list[xla_client.Device]:
  """Returns a list of all devices for a given backend.

  .. currentmodule:: jaxlib._jax

  Each device is represented by a subclass of :class:`Device` (e.g.
  :class:`CpuDevice`, :class:`GpuDevice`). The length of the returned list is
  equal to ``device_count(backend)``. Local devices can be identified by
  comparing :attr:`Device.process_index` to the value returned by
  :py:func:`jax.process_index`.

  If ``backend`` is ``None``, returns all the devices from the default backend.
  The default backend is generally ``'gpu'`` or ``'tpu'`` if available,
  otherwise ``'cpu'``.

  Args:
    backend: This is an experimental feature and the API is likely to change.
      Optional, a string representing the xla backend: ``'cpu'``, ``'gpu'``, or
      ``'tpu'``.

  Returns:
    List of Device subclasses.
  """
  return get_backend(backend).devices()

