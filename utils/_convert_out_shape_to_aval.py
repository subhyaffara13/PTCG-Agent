from typing import Any

def _convert_out_shape_to_aval(out_shape: Any) -> jax_core.AbstractValue:
  match out_shape:
    case jax_core.ShapeDtypeStruct():
      if config._check_vma.value:
        if out_shape.manual_axis_type is None:
          raise ValueError(
              "When `check_vma=True` on `jax.shard_map`, `manual_axis_type` on"
              " `jax.ShapeDtypeStruct` must not be `None`. Please specify how"
              " the output should be varying across mesh axes using the"
              " `manual_axis_type` argument of `jax.ShapeDtypeStruct` or set"
              " `check_vma=False` on `jax.shard_map`.")
        return jax_core.ShapedArray(
            shape=out_shape.shape, dtype=out_shape.dtype,
            sharding=jax_core.get_cur_mesh_sharding(),
            manual_axis_type=out_shape.manual_axis_type)
      return jax_core.ShapedArray(
          shape=out_shape.shape, dtype=out_shape.dtype,
          sharding=jax_core.get_cur_mesh_sharding())
    case MemoryRef():
      return out_shape.get_array_aval()
    case hijax.HiType():
      return out_shape
    case _:
      if type(out_shape) in _out_shape_to_aval_mapping:
        return _out_shape_to_aval_mapping[type(out_shape)](
            out_shape
        )
      if not (hasattr(out_shape, "shape") and hasattr(out_shape, "dtype")):
        raise ValueError(f"Invalid out_shape type: {type(out_shape)}")
      return jax_core.ShapedArray(shape=out_shape.shape, dtype=out_shape.dtype)

