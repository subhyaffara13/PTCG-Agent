
def _extract_aliased_ref(
    ref: RefOrTmemType,
    ref_aval: state_types.AbstractRef,
    transform_avals: Sequence[state_types.Transform],
    transforms: Sequence[state_types.Transform],
    lowering_semantics: mgpu.LoweringSemantics,
) -> tuple[
    RefOrTmemType,
    state_types.AbstractRef,
    Sequence[state_types.Transform],
    Sequence[state_types.Transform],
]:
  i32 = ir.IntegerType.get_signless(32)
  # Looks for the first transform being an ExtractAliasedRef and pulls out the
  # Ref there, updating the transforms.
  match transforms:
    case (
        gpu_core.ExtractAliasedRef(dtype, transformed_shape, offset, alias_group_idx, layout) as t,
        *other_transforms,
    ):
      ref_aval = t.transform_type(ref_aval)
      mlir_dtype = mgpu_utils.dtype_to_ir_type(dtype)
      if isinstance(ref, tcgen05.TMEMRef):
        assert layout is not None
        if ref.shape[0] != transformed_shape[0]:
          raise ValueError(
              "TMEM aliasing only supported for Refs with the same first"
              f" dimension, got {ref.shape[0]} != {transformed_shape[0]}."
          )
        address = arith_dialect.addi(ref.address, _i32_constant(offset))
        ref = tcgen05.TMEMRef(
            address=address,
            shape=cast(tuple[int, int], transformed_shape),
            dtype=mlir_dtype,
            layout=layout,
        )
      else:
        assert isinstance(ref, ir.Value)  # make pyrefly happy
        input_ref_ty = ir.MemRefType(ref.type)
        if input_ref_ty.memory_space == mgpu_utils.smem():
          assert layout is None
          ref_bits = math.prod(transformed_shape) * mgpu_utils.bitwidth(
              mlir_dtype
          )
          if ref_bits % 8:
            raise NotImplementedError("Only byte-aligned bitcasts are supported.")
          assert offset % gpu_core.SMEM_ALIGNMENT == 0

          if lowering_semantics == mgpu.LoweringSemantics.Warpgroup:
            if not isinstance(ref.owner, mgpu.dialect.SliceSMEMOp):
              # This restriction can be lifted by:
              # - Using memref ops to get the pointer and offset of the base ref.
              # - Subtracting gpu_dialect.dynamic_shared_memory() from those to
              #   get the base offset relative to the beginning of SMEM.
              # - Implementing layout and lowering rules for all ops above.
              raise NotImplementedError(
                  "The base ref for aliases must come from a slice_smem op."
              )

            base_offset = ref.owner.offset.value
            total_offset = base_offset + offset

            ref_ty = ir.MemRefType.get(
                transformed_shape, mlir_dtype, memory_space=mgpu_utils.smem()
            )
            slice_op = mgpu.dialect.SliceSMEMOp(ref_ty, total_offset)

            # The composite key formed of `(total_offset, alias_group_idx)` is
            # a unique identifier across:
            #   - different RefUnions (different `total_offset`, since two
            #     distinct RefUnions represent two non-overlapping SMEM
            #     allocations);
            #   - different ref_groups within a RefUnion (different
            #     `alias_group_idx`);
            #   - different elements within a ref_group (different
            #     `total_offset` which is the offset of the particular element to
            #     the beginning of the RefUnion added to the base offset of the
            #     RefUnion). This only holds in the absence of 0-sized refs,
            #     which don't serve a practical purpose anyway.
            slice_op.attributes["alias_id"] = ir.IntegerAttr.get(i32, alias_group_idx)
            ref = slice_op.result
          else:
            ref_bytes = ref_bits // 8
            ref = mgpu.memref_slice(ref, slice(offset, offset + ref_bytes))
            ref = _handle_dtype_bitcast(
                ref,
                ir.MemRefType(ref.type).element_type,
                mlir_dtype,
            )
            ref = mgpu.memref_reshape(ref, transformed_shape)
        elif input_ref_ty.memory_space == mgpu_utils.tmem():

          if isinstance(ref.owner, mgpu.dialect.SliceTmemOp):
            source_slice_op = ref.owner
          elif isinstance(
              ref.owner, mgpu.dialect.TmemLayoutCastOp
          ) and isinstance(ref.owner.operands[0].owner, mgpu.dialect.SliceTmemOp):
            source_slice_op = ref.owner.operands[0].owner
          else:
            raise NotImplementedError(f"Unsupported TMEM ref {ref}.")

          base_offset = source_slice_op.offset.value
          assert isinstance(base_offset, int)  # make pyrefly happy
          total_offset = base_offset + offset
          ref_ty = ir.MemRefType.get(
              transformed_shape, mlir_dtype, memory_space=mgpu_utils.tmem()
          )
          slice_op = mgpu.dialect.SliceTmemOp(ref_ty, ref, total_offset)
          slice_op.attributes["alias_id"] = ir.IntegerAttr.get(i32, alias_group_idx)
          ref = slice_op.result
        else:
          raise NotImplementedError("Unsupported memory space.")
      return (
          ref,
          ref_aval,
          transform_avals[1:],
          tuple(other_transforms),
      )
    case _:
      # No ExtractAliasedRef found, don't do anything.
      return ref, ref_aval, transform_avals, transforms

