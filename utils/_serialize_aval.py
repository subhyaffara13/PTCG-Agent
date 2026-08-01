
def _serialize_aval(
    builder: flatbuffers.Builder, aval: core.ShapedArray
) -> int:
  aval_kind = ser_flatbuf.AbstractValueKind.shapedArray
  shape_offsets = [builder.CreateString(str(d)) for d in aval.shape]
  ser_flatbuf.AbstractValueStartShapeVector(builder, len(aval.shape))
  for d in reversed(shape_offsets):
    builder.PrependUOffsetTRelative(d)
  shape_vector_offset = builder.EndVector()

  ser_flatbuf.AbstractValueStart(builder)
  ser_flatbuf.AbstractValueAddKind(builder, aval_kind)
  ser_flatbuf.AbstractValueAddShape(builder, shape_vector_offset)
  ser_flatbuf.AbstractValueAddDtype(builder, _dtype_to_dtype_kind[aval.dtype])
  ser_flatbuf.AbstractValueAddMemorySpace(builder, _memory_space_to_enum[aval.memory_space])
  return ser_flatbuf.AbstractValueEnd(builder)

