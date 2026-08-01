
def decompress_executable(executable: bytes) -> bytes:
  if zstd:
    return zstd.decompress(executable)
  elif zstandard:
    decompressor = zstandard.ZstdDecompressor()
    return decompressor.decompress(executable)
  else:
    return zlib.decompress(executable)

