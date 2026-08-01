
def _bfloat16_to_float4_e2m1fn_x2(x):
    if x.dtype != torch.bfloat16:
        raise AssertionError(f"Expected x.dtype to be torch.bfloat16, got {x.dtype}")
    x = _f32_to_floatx_unpacked(x.float(), FP4_EBITS, FP4_MBITS)
    x = pack_uint4(x)
    x = x.view(torch.float4_e2m1fn_x2)
    return x

