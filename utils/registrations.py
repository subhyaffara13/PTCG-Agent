
def registrations() -> dict[str, list[tuple[str, Any, int]]]:
  api_version = 1
  return {
      "cpu": [
          (name, value, api_version)
          for name, value in _sparse.registrations().items()
      ]
  }


def registrations() -> dict[str, list[tuple[str, Any, int]]]:
  registrations: dict[str, list[tuple[str, Any, int]]] = {
      "CUDA": [],
      "ROCM": [],
  }
  for platform, module in [("CUDA", _cuda_linalg), ("ROCM", _hip_linalg)]:
    if module:
      registrations[platform].extend(
          (*i, 1) for i in module.registrations().items()
      )
  return registrations


def registrations() -> dict[str, list[tuple[str, Any, int]]]:
  registrations: dict[str, list[tuple[str, Any, int]]] = {
      "CUDA": [],
      "ROCM": [],
  }
  for platform, module in [("CUDA", _cuda_prng), ("ROCM", _hip_prng)]:
    if module:
      registrations[platform].extend(
          (name, value, int(name.endswith("_ffi")))
          for name, value in module.registrations().items()
      )
  return registrations


def registrations() -> dict[str, list[tuple[str, Any, int]]]:
  registrations: dict[str, list[tuple[str, Any, int]]] = {
      "CUDA": [],
      "ROCM": [],
  }
  for platform, module in [("CUDA", _cusolver), ("ROCM", _hipsolver)]:
    if module:
      registrations[platform].extend(
          (name, value, int(name.endswith("_ffi")))
          for name, value in module.registrations().items()
      )
  for platform, module in [("CUDA", _cuhybrid), ("ROCM", _hiphybrid)]:
    if module:
      registrations[platform].extend(
          (*i, 1) for i in module.registrations().items()
      )
  return registrations


def registrations() -> dict[str, list[tuple[str, Any, int]]]:
  registrations: dict[str, list[tuple[str, Any, int]]] = {
      "CUDA": [],
      "ROCM": [],
  }
  for platform, module in [("CUDA", _cusparse), ("ROCM", _hipsparse)]:
    if module:
      registrations[platform].extend(
          (name, value, int(name.endswith("_ffi")))
          for name, value in module.registrations().items()
      )
  return registrations


def registrations() -> dict[str, list[tuple[str, Any, int]]]:
  return {"cpu": [
      (name, value, int(name.endswith("_ffi")))
      for name, value in _lapack.registrations().items()
  ]}

