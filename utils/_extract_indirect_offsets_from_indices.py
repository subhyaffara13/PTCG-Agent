
def _extract_indirect_offsets_from_indices(
    indices: Sequence[Any],
    indices_aval: Sequence[Any],
    core_type: tpu_core.CoreType,
    indexer_shape: tuple[int | Any, ...],
    expected_shape: tuple[int, ...] | None = None,
) -> sc_core.Indices | None:
  """Extracts the indirect offsets from the indices, if there are any.

  Note that it ignores any dimensions other than major. The indices might
  need to be split further to deal with slicing of minor dimensions.
  """
  match indices_aval:
    case [sc_core.Indices(offsets_aval), *_]:
      offsets = indices[0]
      assert isinstance(offsets, sc_core.Indices)
      extracted = _extract_indirect_offsets_from_indices(
          [offsets.values, *indices[1:]],
          [offsets_aval, *indices_aval[1:]],
          core_type,
          indexer_shape,
          expected_shape,
      )
      if extracted is None:
        return None
      return sc_core.Indices(
          extracted.values, ignored_value=offsets.ignored_value
      )

    case [jax_core.AbstractValue() as offsets_aval, *_] if (
        # fmt: off
        isinstance(offsets_aval, state.AbstractRef) or
        (isinstance(offsets_aval, jax_core.ShapedArray) and offsets_aval.shape)
    ):  # fmt: on
      if len(offsets_aval.shape) != 1:
        raise NotImplementedError(
            "Only 1D indices are supported by scatter/gather via"
            " `pltpu.async_copy` on SparseCore, got rank"
            f" {len(offsets_aval.shape)}"
        )
      shape = (*offsets_aval.shape, *indexer_shape[len(offsets_aval.shape) :])
      if expected_shape is not None and shape != expected_shape:
        raise NotImplementedError(
            "The indexer shape in scatter/gather via `pltpu.async_copy` does"
            f" not match the expected shape. Want: {expected_shape}, got:"
            f" {shape}."
        )
      offsets = indices[0]
      assert isinstance(offsets, ir.Value)
    case [state.TransformedRef() as offsets_aval, *_]:
      if offsets_aval.dtype != jnp.dtype("int32"):
        raise NotImplementedError(
            "Only int32 indices are supported by scatter/gather via"
            " `pltpu.async_copy` with a dynamically-shaped indexer"
        )
      offsets_ref = indices[0]
      assert isinstance(offsets_ref, state.TransformedRef)
      offsets, _ = _transform_ref(
          offsets_ref.ref,
          offsets_aval.ref,
          offsets_aval.ref.shape,  # The shape before the indexing.
          offsets_ref.transforms,
      )
      assert isinstance(offsets, ir.Value)
    case _:
      return None

  if isinstance(offsets_aval, (state.AbstractRef, state.TransformedRef)):
    offsets_memory_space = tpu_core.memory_space_to_tpu_memory_space(
        offsets_aval.memory_space, core_type=core_type
    )
    if isinstance(offsets_memory_space, CoreMemorySpace):
      offsets_memory_space = offsets_memory_space.memory_space
    if offsets_memory_space is not MemorySpace.VMEM:
      raise NotImplementedError(
          "Indices for scatter/gather via `pltpu.async_copy` must be in VMEM,"
          f" got {offsets_memory_space!r}"
      )
  return sc_core.Indices(offsets)

