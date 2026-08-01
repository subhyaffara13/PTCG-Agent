
def _handle_dtype_bitcast(
    ref: ir.Value, src_dtype: ir.Type, dst_dtype: ir.Type
) -> ir.Value:
  """Allows bitcasting a SMEM ref from one element type to another.

  Args:
    ref: the reference to bitcast.
    src_dtype: the source element type.
    dst_dtype: the destination element type.

  Returns:
    A bitcasted version of `ref` with element type `dst_dtype`.

  Raises:
    ValueError: if the source ref is not in SMEM.
  """
  if src_dtype == dst_dtype:
    return ref
  if src_dtype != ir.IntegerType.get_signless(8):
    raise NotImplementedError(
        "Data type bitcast is only supported from i8 to other types."
    )
  ref_ty = ir.MemRefType(ref.type)
  if not mgpu_utils.is_smem_ref(ref_ty):
    raise ValueError(f"Only workgroup memory is supported but got {ref}.")
  if len(ref_ty.shape) != 1:
    raise NotImplementedError(
        "Data type bitcast is only supported for 1D arrays."
    )
  [stride], _ = ref_ty.get_strides_and_offset()
  if stride != 1:
    raise ValueError(
        "Data type bitcast is only supported for contiguous 1D arrays, but got "
        f"stride={stride}."
    )
  [shape_bytes] = ref_ty.shape
  shape_bitwidth = shape_bytes * 8
  target_bitwidth = mgpu_utils.bitwidth(dst_dtype)

  if shape_bitwidth % target_bitwidth:
    raise ValueError(
        f"Can not bitcast memory region of size {shape_bitwidth} bits to dtype "
        f"with {target_bitwidth} bits."
    )

  result_type = ir.MemRefType.get(
      shape=(shape_bitwidth // target_bitwidth,),
      element_type=dst_dtype,
      memory_space=ref_ty.memory_space,
  )

  # Do a memref_ptr/ptr_as_memref roundtrip instead of using `memref.view`,
  # which refuses to take in our source ref. This is because `memref.view` only
  # works on a super restricted set of `memref`s. E.g., it does not work if an
  # offset is specified, which can be the case for our SMEM refs.
  return mgpu_utils.ptr_as_memref(mgpu_utils.memref_ptr(ref), result_type)

