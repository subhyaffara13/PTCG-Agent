
def compress_executable(executable: bytes) -> bytes:
  if zstd:
    return zstd.compress(executable)
  elif zstandard:
    compressor = zstandard.ZstdCompressor()
    return compressor.compress(executable)
  else:
    return zlib.compress(executable)

