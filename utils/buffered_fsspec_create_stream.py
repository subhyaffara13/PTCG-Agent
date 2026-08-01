
def buffered_fsspec_create_stream(
    path: str | os.PathLike[str], mode: str
) -> Generator[io.IOBase, None, None]:
  """Buffered create_stream to support torch.save on non-POSIX filesystems."""
  if mode == "wb":
    stream = ProtectedBytesIO()
    try:
      yield cast(io.IOBase, stream)
      stream.seek(0)
      # Write the full buffer to GCS in one go
      with epath.Path(path).open("wb") as f:
        f.write(stream.getvalue())
    finally:
      stream.force_close()
  else:
    # For reading, we can stream directly or buffer.
    # Buffering is safer for some GCS versions.
    stream = io.BytesIO()
    with epath.Path(path).open("rb") as f:
      stream.write(f.read())
    stream.seek(0)
    yield cast(io.IOBase, stream)

