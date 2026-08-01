
def _prepare_dma_refs(
    src_ref,
    dst_ref,
    src_aval,
    dst_aval,
    core_type: tpu_core.CoreType,
    is_add: bool = False,
):
  """Prepares the DMA source and destination references."""
  src_ref_orig, dst_ref_orig = src_ref, dst_ref
  src_memory_space = tpu_core.memory_space_to_tpu_memory_space(
      src_aval.memory_space, core_type
  )
  dst_memory_space = tpu_core.memory_space_to_tpu_memory_space(
      dst_aval.memory_space, core_type
  )
  src_ref, src_transforms = _get_ref_and_transforms(src_ref)
  dst_ref, dst_transforms = _get_ref_and_transforms(dst_ref)
  src_aval, src_transforms_aval = _get_ref_and_transforms(src_aval)
  dst_aval, dst_transforms_aval = _get_ref_and_transforms(dst_aval)
  match src_memory_space, dst_memory_space:
    case MemorySpace.HBM | MemorySpace.VMEM_SHARED, MemorySpace.VMEM:
      if _has_indirect_offsets(dst_transforms, dst_transforms_aval, core_type):
        raise ValueError(
            "Only the source ref can be indexed when doing a gather via"
            " `pltpu.async_copy`"
        )
      dst_ref, _ = _transform_ref(
          dst_ref, dst_aval, dst_aval.shape, dst_transforms
      )
      dst_ref_shape = tuple(ir.MemRefType(dst_ref.type).shape)
      indirect_offsets, src_transforms = _extract_indirect_offsets(
          src_transforms, dst_ref_shape, src_transforms_aval, core_type
      )
      src_ref, _ = _transform_ref(
          src_ref, src_aval, src_aval.shape, src_transforms
      )
      indirect_offsets_ref_str = "src_ref"
    case MemorySpace.VMEM, MemorySpace.HBM | MemorySpace.VMEM_SHARED:
      if _has_indirect_offsets(src_transforms, src_transforms_aval, core_type):
        raise ValueError(
            "Only the destination ref can be indexed when doing a scatter via"
            " `pltpu.async_copy`"
        )
      src_ref, _ = _transform_ref(
          src_ref, src_aval, src_aval.shape, src_transforms
      )
      src_ref_shape = tuple(ir.MemRefType(src_ref.type).shape)
      indirect_offsets, dst_transforms = _extract_indirect_offsets(
          dst_transforms, src_ref_shape, dst_transforms_aval, core_type
      )
      dst_ref, _ = _transform_ref(
          dst_ref, dst_aval, dst_aval.shape, dst_transforms
      )
      indirect_offsets_ref_str = "dst_ref"
    case _:  # Indirect DMA is not supported.
      if (
          # fmt: off
          _has_indirect_offsets(src_transforms, src_transforms_aval, core_type) or
          _has_indirect_offsets(dst_transforms, dst_transforms_aval, core_type)
          # fmt: on
      ):
        raise NotImplementedError(
            "Scatter/gather via `pltpu.async_copy` from"
            f" {src_memory_space!r} to {dst_memory_space!r} is not"
            " supported"
        )
      if is_add:
        raise ValueError(
            "DMAs with `add=True` are only supported between VMEM and "
            f"HBM/VMEM_SHARED."
            f"Got (src, dst)={(src_aval.memory_space, dst_aval.memory_space)}"
        )
      indirect_offsets = None
      indirect_offsets_ref_str = ""
  if is_add and indirect_offsets is None:
    raise NotImplementedError(
        "DMAs with `add=True` must (for now) specify offsets of the"
        " majormost dimension. You can do this by writing"
        " `pltpu.async_copy(..., {ref}={ref}.at[jnp.arange(vec_dim)], ...)`"
        " or `pltpu.async_copy(..., {ref}={ref}.at[indices_ref],"
        " ...)`.".format(ref=indirect_offsets_ref_str)
    )
  if indirect_offsets is None:
    # If typical DMA path, don't alter the refs.
    return src_ref_orig, dst_ref_orig, None
  return src_ref, dst_ref, indirect_offsets

