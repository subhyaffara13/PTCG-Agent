import math


def _device_id_dict_to_mesh(mesh_context: pallas_utils.MeshInfo | None, device_id_dict, get_axis_index):
  if mesh_context is None:
    mesh_axis_sizes = {}
  else:
    mesh_axis_sizes = dict(
        zip(mesh_context.axis_names, mesh_context.mesh_shape)
    )
  physical_axis_dict = {}
  # Handle joint axes (i.e., one logical axis over >1 physical axes)
  for axis_name, idx in device_id_dict.items():
    if isinstance(axis_name, tuple) and any(
        a in mesh_axis_sizes for a in axis_name
    ):
      if not all(a in mesh_axis_sizes for a in axis_name):
        raise NotImplementedError(
            f"{axis_name} mixes JAX mesh and Pallas mesh grid axes"
        )
      axes_dimensions = [mesh_axis_sizes[name] for name in axis_name]
      for axis_index, axis_name in enumerate(axis_name):
        axis_size = mesh_axis_sizes[axis_name]
        inner_mesh_size = math.prod(axes_dimensions[axis_index + 1 :])

        # Fast path for power of 2s
        if inner_mesh_size & (inner_mesh_size - 1) == 0:
          shift_len = (inner_mesh_size & -inner_mesh_size).bit_length() - 1
          partial_device_idx = idx >> shift_len
        else:
          partial_device_idx = idx // inner_mesh_size

        if axis_size & (axis_size - 1) == 0:
          device_idx = partial_device_idx & jnp.asarray(
              axis_size - 1, dtype=partial_device_idx.dtype
          )
        else:
          device_idx = lax.rem(partial_device_idx, axis_size)
        physical_axis_dict[axis_name] = device_idx
    else:
      physical_axis_dict[axis_name] = idx
  device_id = []
  for axis_name in mesh_axis_sizes:
    if axis_name in physical_axis_dict:
      device_id.append(physical_axis_dict[axis_name])
    else:
      device_id.append(get_axis_index(axis_name))
  non_mesh_axes = {
      k: v
      for k, v in physical_axis_dict.items()
      if k not in mesh_axis_sizes
  }
  return tuple(device_id), non_mesh_axes


def _device_id_dict_to_mesh(device_id_dict, axis_sizes, axis_indices):
  physical_axis_dict = {}
  axis_names = axis_sizes.keys()
  for axis, idx in device_id_dict.items():
    if isinstance(axis, tuple) and any(a in axis_names for a in axis):
      if not all(a in axis_names for a in axis):
        raise NotImplementedError(
            f"{axis} mixes JAX mesh and Pallas mesh grid axes"
        )
      axes_dimensions = [axis_sizes[name] for name in axis]
      for axis_index, axis_name in enumerate(axis):
        axis_size = axis_sizes[axis_name]
        inner_mesh_size = math.prod(axes_dimensions[axis_index + 1 :])
        minor_divisor = inner_mesh_size

        # Fast path for power of 2s
        if inner_mesh_size & (inner_mesh_size - 1) == 0:
          shift_len = (inner_mesh_size & -inner_mesh_size).bit_length() - 1
          partial_device_idx = idx >> shift_len
        else:
          partial_device_idx = idx // minor_divisor

        if axis_size & (axis_size - 1) == 0:
          device_idx = partial_device_idx & (axis_size - 1)
        else:
          device_idx = partial_device_idx % axis_size
        physical_axis_dict[axis_name] = device_idx
    else:
      physical_axis_dict[axis] = idx
  device_id = []
  for axis in axis_names:
    if axis in physical_axis_dict:
      device_id.append(physical_axis_dict[axis])
    else:
      device_id.append(axis_indices[axis])
  non_mesh_axes = {
      k: v for k, v in physical_axis_dict.items() if k not in axis_names
  }
  return tuple(device_id), non_mesh_axes

