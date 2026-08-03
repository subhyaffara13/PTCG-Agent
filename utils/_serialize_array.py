from typing import Callable

def _serialize_array(
    builder: flatbuffers.Builder,
    serialize_one: Callable[[flatbuffers.Builder, T], int],
    elements: Iterable[T],
) -> int:
  element_offsets = [serialize_one(builder, e) for e in elements]
  del elements
  ser_flatbuf.PyTreeDefStartChildrenVector(builder, len(element_offsets))
  for sc in reversed(element_offsets):
    builder.PrependUOffsetTRelative(sc)
  return builder.EndVector()

