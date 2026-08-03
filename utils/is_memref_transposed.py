import math


def is_memref_transposed(ref: ir.MemRefType) -> bool:
  strides, _ = ref.get_strides_and_offset()
  prev_stride = math.inf
  for stride in strides:
    if stride > prev_stride:
      return True
    prev_stride = stride
  return False

