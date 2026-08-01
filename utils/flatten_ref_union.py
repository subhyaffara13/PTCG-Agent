
def flatten_ref_union(ref_union: AbstractRefUnion) -> tuple[_Ref, ...]:
  """Flattens a union of trees of references into a tuple of references.

  This is the moral equivalent of `jax.tree.leaves` for aliased references.
  """
  flat_refs = []
  if ref_union.memory_space == SMEM:
    union_bytes = 0
    for group_idx, ref_group in enumerate(ref_union.refs):
      byte_offset = 0
      def unflatten(ref):
        nonlocal byte_offset
        byte_offset = align_to(byte_offset, SMEM_ALIGNMENT)
        assert isinstance(ref, state.AbstractRef) or isinstance(
            ref, pallas_core.TransformedRef
        )
        if not isinstance(ref, pallas_core.TransformedRef):
          ref = pallas_core.TransformedRef(ref, transforms=())
        transform = ExtractAliasedRef.from_transformed_ref(ref, byte_offset, group_idx)
        result = pallas_core.TransformedRef(
            ref_union, transforms=(transform, *ref.transforms)
        )
        if jnp.issubdtype(ref.dtype, jnp.integer):
          nbits = jnp.iinfo(ref.dtype).bits
        elif jnp.issubdtype(ref.dtype, jnp.floating):
          nbits = jnp.finfo(ref.dtype).bits
        else:
          raise NotImplementedError(f"Unsupported dtype: {ref.dtype}")
        ref_bits = math.prod(ref.shape) * nbits
        if ref_bits % 8:
          raise ValueError(
              "Only byte-aligned shapes are supported. Got shape:"
              f" {ref.dtype}{ref.shape}"
          )
        byte_offset += ref_bits // 8
        return result
      flat_refs.append(jax.tree.map(unflatten, ref_group))
      union_bytes = max(union_bytes, byte_offset)
    assert union_bytes == ref_union.shape[0]
  elif ref_union.memory_space == TMEM:
    union_cols = 0
    for group_idx, ref_group in enumerate(ref_union.refs):
      col_offset = 0
      def unflatten(ref):
        nonlocal col_offset
        col_offset = align_to(col_offset, TMEM_COL_ALIGNMENT)
        if not isinstance(ref, pallas_core.TransformedRef):
          ref = pallas_core.TransformedRef(ref, transforms=())
        ncols = ref.layout.cols_in_shape(ref.shape,
                                         dtypes.itemsize_bits(ref.dtype))
        transform = ExtractAliasedRef.from_transformed_ref(
            ref, col_offset, group_idx, layout=ref.layout)
        result = pallas_core.TransformedRef(
            ref_union, transforms=(transform, *ref.transforms)
        )
        col_offset += ncols
        return result
      flat_refs.append(jax.tree.map(unflatten, ref_group))
      union_cols = max(union_cols, col_offset)
    assert union_cols == ref_union.shape[1], (union_cols, ref_union.shape[1])
  else:
    raise NotImplementedError("Only SMEM and TMEM refs are supported.")
  return tuple(flat_refs)

