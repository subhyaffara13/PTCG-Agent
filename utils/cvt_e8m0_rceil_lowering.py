import functools

def cvt_e8m0_rceil_lowering(inp):
    """
    Lowering for cvt_e8m0_rceil. Uses PTX cvt.rp.satfinite.ue8m0x2.f32 on SM100+.

    The PTX instruction takes 2 float32 and outputs 2 e8m0 packed in uint16.
    Currently we pass 0.0 as the second input and only use the low byte result.
    """
    # TODO: Optimize to process pairs (pack=2) by creating a custom Pointwise
    # that loads adjacent elements, applies PTX to both, and uses a follow-up
    # kernel to extract the packed uint16 results as uint8.
    if not _is_sm100_or_later():
        raise NotImplementedError(
            "cvt_e8m0_rceil requires SM100+ (Blackwell) for PTX instruction support"
        )

    dtype = inp.get_dtype()
    if dtype not in (torch.float32, torch.float16, torch.bfloat16):
        raise ValueError(
            f"cvt_e8m0_rceil requires float32, float16, or bfloat16 input, got {dtype}"
        )

    # Upcast bf16/fp16 to float32 for PTX instruction
    if dtype != torch.float32:
        inp = to_dtype(inp, torch.float32)

    fn = functools.partial(
        ops.inline_asm_elementwise,
        asm="cvt.rp.satfinite.ue8m0x2.f32 $0, 0.0, $1;",
        constraints="=h,r",
        dtype=torch.uint16,
        is_pure=True,
        pack=1,
    )
    result = make_pointwise(fn)(inp)
    return to_dtype(result, torch.uint8)

