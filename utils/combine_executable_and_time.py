
def combine_executable_and_time(
    serialized_executable: bytes, compile_time: int
) -> bytes:
  """Given the serialized executable and the compilation time, produce a cache
  entry in the format shown below.

  The cache entry is of the form:
  Byte:     0    1    2    3    4 ...
  Content:  compilation time    serialized executable
            (big-endian int)
  """
  return (
      int(compile_time).to_bytes(_TIME_BYTES, byteorder="big")
      + serialized_executable
  )

