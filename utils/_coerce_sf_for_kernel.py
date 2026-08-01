
def _coerce_sf_for_kernel(sf: torch.Tensor, expected_mn: int | None = None) -> torch.Tensor:
    """Lay out `sf` as DeepGEMM's `check_sf_layout` expects: MN-major
    (`stride(-2) == 1`) and TMA-aligned (`stride(-1) == align(mn, 16/esize)`).

    Inputs come in three flavors:
      - `float8_e8m0fnu` on SM100: raw UE8M0 bytes — pack 4 K-bytes → int32
        (last dim /4) for the kernel's `(INT, 1, gran_k)` path.
      - `float8_e8m0fnu` on SM90: SM90 dispatch only accepts FP32 SFs, so cast
        UE8M0 → FP32 (exact upcast — UE8M0 is the biased-exponent half of a
        pow-of-2 FP32, so `.float()` rebuilds the original FP32 scale exactly).
      - `float32`: per-token / per-block SFs from `per_token_cast_to_fp8` or
        on-disk weights — round to UE8M0 on SM100 (see `_ceil_to_ue8m0`).
      - `int32`: already-packed UE8M0 — pass through.

    When `expected_mn` is set and the SF's M-dim is smaller (block-quantized
    UE8M0, e.g. DSv4-Flash compressor weights with `(N/128, K/128)` SFs), we
    repeat the SF on the M-axis to per-row before packing — the `(INT, 1, gran_k)`
    DeepGEMM kernel branch is the only UE8M0 path on SM100; for `gran_mn > 1`
    the kernel only handles FP32 SFs and would otherwise reject our INT SF here.
    """
    is_sm100 = _is_sm100(sf.device)
    if sf.dtype == torch.float8_e8m0fnu:
        if expected_mn is not None and sf.size(-2) < expected_mn:
            gran_mn = expected_mn // sf.size(-2)
            sf = sf.repeat_interleave(gran_mn, dim=-2)
        if is_sm100:
            sf = sf.contiguous().view(torch.int32)
        else:
            sf = sf.float()
    elif sf.dtype == torch.float32 and is_sm100:
        sf = _ceil_to_ue8m0(sf)

    if sf.dim() not in (2, 3):
        raise ValueError(f"DeepGEMM SF must be 2D or 3D, got {sf.dim()}D")

    mn = sf.size(-2)
    kf = sf.size(-1)
    align_to = 16 // sf.element_size()  # `get_tma_aligned_size`: align(mn, 16 / element_size)
    aligned_mn = -(-mn // align_to) * align_to
    target_strides = (1, aligned_mn) if sf.dim() == 2 else (kf * aligned_mn, 1, aligned_mn)

    if tuple(sf.stride()) == target_strides:
        return sf
    out = torch.empty_strided(sf.shape, target_strides, dtype=sf.dtype, device=sf.device)
    out.copy_(sf)
    return out

