
def _maybe_convert_to_slice(
    indexer: indexing.NDIndexer
) -> list[tuple[int, int, int]] | None:
  args = []

  for i in indexer.indices:
    if not isinstance(i, indexing.Slice):
      return None

    start = i.start
    end = i.start + (i.size - 1) * i.stride + 1
    stride = i.stride

    # cannot convert to static `slice` if `start` or `end` is dynamic
    if not isinstance(start, int) or not isinstance(end, int):
      return None

    args.append((start, end, stride))

  return args

