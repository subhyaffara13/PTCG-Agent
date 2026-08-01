
def get_kernel_name(g: NativeFunctionsGroup, backend_index: BackendIndex) -> str:
    kernel = backend_index.get_kernel(g.functional)
    if g.structured or kernel is None:
        return cpp.name(g.functional.func)
    return kernel.kernel


def get_kernel_name(
    is_mqa: bool,
    save_residuals: bool,
    is_segmented: bool,
    phase: str,
) -> str:
  """Returns a unique name for all SplashAttention kernel variants."""
  assert phase == "dq" or phase == "dkv" or phase == "fwd"
  # Saving residuals is supported only for the fwd phase.
  assert not save_residuals or phase == "fwd"
  residuals = "_residuals" if save_residuals else "_no_residuals"
  attention_type = "mqa" if is_mqa else "mha"
  segments = "_segmented" if is_segmented else ""
  return f"splash_{attention_type}_{phase}{segments}{residuals}"

