
def _get_barrier_base_index(aval, transforms) -> ir.Value | None:
  if not transforms:
    return None
  strides = list(pallas_utils.strides_from_shape(aval.shape))
  base_index: ir.Value | None = None
  while transforms:
    match transforms:
      case [indexing.NDIndexer() as indexer, *transforms]:
        num_int_idxs = 0
        for i, (idx, stride) in enumerate(zip(indexer.indices, strides[:])):
          if isinstance(idx, indexing.Slice):
            if idx.stride != 1:
              raise NotImplementedError(
                  "Barrier does not support slice with `stride != 1`"
              )
            idx = idx.start
          else:
            # This dimension is absent for any corresponding `NDIndexer`s, so
            # we remove the corresponding stride.
            strides.pop(i - num_int_idxs)
            num_int_idxs += 1

          if isinstance(
              idx, (int, ir.Value, mgpu.FragmentedArray, literals.TypedNdArray)
          ):
            idx = lowering._as_index(idx)  # pylint: disable=protected-access
          else:
            raise ValueError(
                "Barrier can only be indexed with integers or slices, got"
                f" {idx}"
            )

          idx = arith_dialect.muli(idx, lowering._as_index(stride))  # pylint: disable=protected-access
          if base_index is None:
            base_index = idx
          else:
            base_index = arith_dialect.addi(base_index, idx)
      case _:
        raise ValueError("Barrier does not support arbitrary transforms")
  return base_index

