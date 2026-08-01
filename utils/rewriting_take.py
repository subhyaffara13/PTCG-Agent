
def rewriting_take(
    arr: Array,
    idx: Index | tuple[Index, ...], *,
    indices_are_sorted: bool = False,
    unique_indices: bool = False,
    mode: str | slicing.GatherScatterMode | None = None,
    fill_value: ArrayLike | None = None,
    normalize_indices: bool = True,
    out_sharding: NamedSharding | PartitionSpec | None = None,
    strategy: IndexingStrategy = IndexingStrategy.AUTO,
) -> Array:
  # Computes arr[idx].
  # All supported cases of indexing can be implemented as an XLA gather,
  # followed by an optional reverse and broadcast_in_dim.
  indexer = NDIndexer.from_raw_indices(idx, arr.shape)

  if not isinstance(strategy, IndexingStrategy):
    raise TypeError(f"Expected strategy to be IndexingStrategy; got {strategy}")

  if config.check_static_indices.value and (mode is None or slicing.GatherScatterMode.from_any(mode) == slicing.GatherScatterMode.PROMISE_IN_BOUNDS):
    indexer.validate_static_indices(normalize_indices=normalize_indices)

  if strategy == IndexingStrategy.STATIC_SLICE:
    static_slice_indexer = indexer.to_static_slice(
      arr_is_sharded=indexer.is_sharded(arr),
      normalize_indices=normalize_indices,
      mode=mode)
    return _static_slice(arr, static_slice_indexer)

  if strategy == IndexingStrategy.DYNAMIC_SLICE:
    dynamic_slice_indexer = indexer.to_dynamic_slice(
      arr_is_sharded=indexer.is_sharded(arr),
      normalize_indices=normalize_indices,
      mode=mode)
    return _dynamic_slice(arr, dynamic_slice_indexer)

  if strategy == IndexingStrategy.AUTO:
    # Attempt static slice first
    try:
      static_slice_indexer = indexer.to_static_slice(
        arr_is_sharded=indexer.is_sharded(arr),
        normalize_indices=normalize_indices,
        mode=mode)
    except (TypeError, ValueError, IndexError):
      pass
    else:
      return _static_slice(arr, static_slice_indexer)

    # Attempt dynamic slice next
    try:
      dynamic_slice_indexer = indexer.to_dynamic_slice(
        arr_is_sharded=indexer.is_sharded(arr),
        normalize_indices=normalize_indices,
        mode=mode)
    except (TypeError, ValueError, IndexError):
      pass
    else:
      return _dynamic_slice(arr, dynamic_slice_indexer)

  # In remaining cases, compute via gather.
  indexer = indexer.expand_bool_indices()
  dynamic_idx, treedef = tree_flatten(indexer)
  internal_gather = partial(
      _gather, treedef=treedef,
      indices_are_sorted=indices_are_sorted, unique_indices=unique_indices,
      mode=mode, fill_value=fill_value, normalize_indices=normalize_indices)
  if out_sharding is not None:
    out_sharding = canonicalize_sharding(out_sharding, 'take')
    return auto_axes(internal_gather, out_sharding=out_sharding,
                     axes=out_sharding.mesh.explicit_axes,
                     )(arr, dynamic_idx)
  return internal_gather(arr, dynamic_idx)

