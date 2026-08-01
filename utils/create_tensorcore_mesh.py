
def create_tensorcore_mesh(
    axis_name: str,
    devices: Sequence[jax.Device] | None = None,
    num_cores: int | None = None,
) -> TensorCoreMesh:
  if devices is not None and num_cores is not None:
    raise ValueError("cannot specify both devices and num_cores")
  if num_cores is None:
    if devices is None:
      abstract_device = jax.sharding.get_abstract_mesh().abstract_device
      if abstract_device is None:
        devices = [jax.devices()[0]]
      else:
        devices = [abstract_device]
    num_cores = devices[0].num_cores
  return TensorCoreMesh(
      np.array([TensorCore(i) for i in range(num_cores)]),
      [axis_name],
  )

