
def _cvt_e8m0_rceil_aten(inp: Tensor) -> Tensor:
    """
    Convert float to e8m0 format with ceiling rounding and satfinite semantics.

    e8m0 format: 8-bit biased exponent (bias=127), no mantissa.
    For MX format scaling, this extracts the exponent with ceiling rounding.
    Uses satfinite semantics: inf is saturated to 254 (max finite e8m0).
    Accepts float32, float16, or bfloat16 (upcasted to float32 internally).
    """
    if inp.dtype not in (torch.float32, torch.float16, torch.bfloat16):
        raise ValueError(
            f"cvt_e8m0_rceil requires float32, float16, or bfloat16 input, got {inp.dtype}"
        )
    if inp.dtype != torch.float32:
        inp = inp.to(torch.float32)
    inp_bits = inp.view(torch.int32)
    biased_exp = (inp_bits >> 23) & 0xFF
    mantissa = inp_bits & 0x7FFFFF
    needs_round_up = mantissa != 0
    e8m0_biased = biased_exp + needs_round_up.to(torch.int32)
    # satfinite: clamp to max finite e8m0 value (254), not 255 (inf/nan)
    e8m0_biased = torch.clamp(e8m0_biased, 0, 254)
    return e8m0_biased.to(torch.uint8)

