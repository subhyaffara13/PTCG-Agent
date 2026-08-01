
def _chunk_iter(read: t.Callable[[int], bytes], size: int) -> t.Iterator[bytes | None]:
    """Read data in chunks for multipart/form-data parsing. Stop if no data is read.
    Yield ``None`` at the end to signal end of parsing.
    """
    while True:
        data = read(size)

        if not data:
            break

        yield data

    yield None


def _chunk_iter(x, size):
  if size > x.shape[0]:
    yield x
  else:
    num_chunks, tail = ufuncs.divmod(x.shape[0], size)
    for i in range(num_chunks):
      yield lax_slicing.dynamic_slice_in_dim(x, i * size, size)
    if tail:
      yield lax_slicing.dynamic_slice_in_dim(x, num_chunks * size, tail)

