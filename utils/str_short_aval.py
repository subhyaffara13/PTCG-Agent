
def str_short_aval(shape, dtype, mesh, spec, mat, memory_space,
                   short_dtypes=False, mesh_axis_types=False) -> str:
  dt_str = dtypes.short_dtype_name(dtype) if short_dtypes else dtype.name
  dt_str = dt_str.replace('void', 'float0')
  shapestr = _get_shape_sharding_str(shape, spec)
  mesh_axes = f'({_axis_types_dict(mesh)})' if mesh_axis_types else ''
  vma_ur = _vma_ur_str(mat, spec.unreduced, spec.reduced, mesh)
  ms_str = ("" if memory_space == MemorySpace.Device else
            f"<{memory_space.name.lower()}>")
  return f'{dt_str}{ms_str}[{shapestr}]{vma_ur}{mesh_axes}'

