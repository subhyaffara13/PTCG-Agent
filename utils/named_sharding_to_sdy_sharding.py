
def named_sharding_to_sdy_sharding(self, num_dimensions: int,
                                   modify_wrt_axis_types: bool) -> SdyArray:
  dim_shardings = [SdyDim(axes=(), is_open=False)] * num_dimensions
  for i, dim_spec in enumerate(self.spec.partitions):
    if dim_spec is PartitionSpec.UNCONSTRAINED:
      dim_shardings[i] = SdyDim(axes=(), is_open=True)
    elif dim_spec is None:
      # Already empty and closed sharding.
      pass
    else:
      dim_spec = dim_spec if isinstance(dim_spec, tuple) else (dim_spec,)
      dim_shardings[i] = SdyDim(axes=dim_spec, is_open=False)

  explicit_replicated_axes = frozenset()
  if modify_wrt_axis_types and self.mesh._any_axis_auto:
    dim_shardings = [d.replace(is_open=True) for d in dim_shardings]
    explicit_replicated_axes = frozenset(
        r for r in self.replicated_axes
        if self.mesh._name_to_type[r] == mesh_lib.AxisType.Explicit)

  return SdyArray(mesh_shape=self.mesh.shape_tuple,
                  dim_shardings=tuple(dim_shardings),
                  logical_device_ids=self._logical_device_ids,
                  replicated_axes=explicit_replicated_axes,
                  unreduced_axes=self.spec.unreduced)

