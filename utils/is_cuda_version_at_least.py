
def is_cuda_version_at_least(major: int, minor: int) -> bool:
  assert 0 <= major
  assert 0 <= minor < 100
  return (
      cuda_versions is not None
      and cuda_versions.cuda_runtime_get_version() >= major * 1000 + minor * 10
  )

