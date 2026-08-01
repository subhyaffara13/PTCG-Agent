
def _select_fp8_cast_kwargs(
    weight: torch.Tensor, weight_scale_inv: torch.Tensor, block_size: tuple | None, is_sm100: bool
) -> dict:
    """Pick the `per_token_cast_to_fp8` kwargs from weight dtype + SF dtype + arch.

    Cases mirror the kernel's recipes:
      - FP4 weights (`int8`): gran_k=32 packed-UE8M0 SF. SM100+ only.
      - FP8 weights + UE8M0 SF on SM100: gran_k=128 packed-UE8M0 SF (DSv4).
      - FP8 weights + UE8M0 SF on SM90: gran_k=128 FP32 SF — the SM90 dispatch in
        `layout.hpp` only matches FP32 SFs, so we keep act SFs as FP32 (and float
        the weight SF in `_coerce_sf_for_kernel`; UE8M0 → FP32 is an exact upcast).
      - FP8 weights + float SF: gran_k=128 float SF (DSv3).
    """
    if weight.dtype == torch.int8:  # FP4
        return {"use_ue8m0": True, "gran_k": 32, "use_packed_ue8m0": True}
    # FP8 weights: validate block_size (informational; kernel infers recipe from SF dtype/shape).
    if block_size is None:
        raise ValueError(
            "DeepGEMM requires block-wise quantized FP8 weights, but the experts have no `block_size` set."
        )
    block_size = tuple(block_size)
    if block_size not in ((128, 128), (1, 128)):
        raise ValueError(f"DeepGEMM requires `block_size` ∈ {{(128, 128), (1, 128)}}, got {block_size}.")
    if weight_scale_inv.dtype == torch.float8_e8m0fnu and is_sm100:
        return {"use_ue8m0": True, "gran_k": 128, "use_packed_ue8m0": True}
    return {"use_ue8m0": False, "gran_k": 128}

