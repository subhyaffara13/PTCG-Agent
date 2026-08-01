
def extract_executable_and_time(
    executable_and_time: bytes
) -> tuple[bytes, int]:
  """Given the cache entry in the format shown below, extract the serialized
  executable and the compilation time.

  The cache entry 'executable_and_time' is of the form:
  Byte:     0    1    2    3    4 ...
  Content:  compilation time    serialized executable
            (big-endian int)
  """
  return executable_and_time[_TIME_BYTES:], int.from_bytes(
      executable_and_time[:_TIME_BYTES], byteorder='big')

