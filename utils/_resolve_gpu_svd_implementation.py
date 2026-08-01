
def _resolve_gpu_svd_implementation(
    ctx: mlir.LoweringRuleContext,
    target_name_prefix: str,
    algorithm: SvdAlgorithm | None,
    m: core.DimSize,
    n: core.DimSize,
) -> _GpuSvdImpl:
  """Map ``algorithm`` (and DEFAULT) to the concrete GPU SVD implementation."""
  if algorithm is None:
    algorithm = SvdAlgorithm.DEFAULT

  if algorithm == SvdAlgorithm.QR:
    return _GpuSvdImpl.QR_GESVD
  if algorithm == SvdAlgorithm.JACOBI:
    return _GpuSvdImpl.JACOBI
  if algorithm == SvdAlgorithm.POLAR:
    return _GpuSvdImpl.POLAR
  if algorithm == SvdAlgorithm.DIVIDE_AND_CONQUER:
    if target_name_prefix != "hip":
      raise NotImplementedError(
          "Divide-and-conquer SVD (SvdAlgorithm.DIVIDE_AND_CONQUER) is only "
          "supported on AMD (ROCm) GPUs, not on NVIDIA CUDA.")
    return _GpuSvdImpl.GESDD

  if algorithm != SvdAlgorithm.DEFAULT:
    raise NotImplementedError(
        f"Unsupported SVD algorithm on GPU: {algorithm!r}")

  if target_name_prefix in ["cu", "hip"]:
    try:
      if m <= 1024 and n <= 1024:
        return _GpuSvdImpl.JACOBI
    except core.InconclusiveDimensionOperation:
      pass
    return _GpuSvdImpl.GESVD

  raise AssertionError(
      f"Unexpected GPU target_name_prefix for SVD: {target_name_prefix!r}")

