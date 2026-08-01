
def _deserialize_aval(aval: ser_flatbuf.AbstractValue, *,
                      scope: shape_poly.SymbolicScope,
                      sharding: named_sharding.NamedSharding | None,
                      ) -> core.ShapedArray:
  dtype = _dtype_kind_to_dtype[aval.Dtype()]
  shape = shape_poly.symbolic_shape(
      ",".join(
            aval.Shape(i).decode("utf-8") for i in range(aval.ShapeLength())
        ),
        scope=scope
    )
  if (ser_mem_space := aval.MemorySpace()):
    mem_space = _memory_space_from_enum[ser_mem_space]
  else:
    mem_space = core.MemorySpace.Device

  return core.update_aval_with_sharding(
      core.ShapedArray(shape, dtype, memory_space=mem_space), sharding
  )

