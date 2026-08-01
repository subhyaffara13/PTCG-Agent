
def tpu_generation() -> int:
  """Generation number of the currently attached TPU."""
  if version := _TPU_KIND_PATTERN.match(tpu_kind()):
    return int(version[2])
  raise NotImplementedError("only TPU devices are supported")

