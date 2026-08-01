
def _result_avals(results: Sequence[ResultMetadata]) -> tuple[core.AbstractValue, ...]:
  avals: list[core.AbstractValue] = []
  for idx, result in enumerate(results):
    if result is core.abstract_token:
      avals.append(result)
    else:
      if not hasattr(result, "shape") or not hasattr(result, "dtype"):
        raise ValueError(
            "All elements of result_shape_dtypes must have 'shape' and 'dtype' "
            f"attributes. Got {result} at position {idx}.")
      # Update the dtype because shaped_abstractify can canonicalize the dtype.
      # We need to call shaped_abstractify here to handle sharding, vma and
      # memory_kind bits.
      # TODO(yashkatariya): Maybe add an option to shaped_abstractify/typeof
      # to not canonicalize dtype.
      avals.append(core.shaped_abstractify(result).update(dtype=result.dtype))
  return tuple(avals)

