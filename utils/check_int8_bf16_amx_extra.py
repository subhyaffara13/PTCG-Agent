
def check_int8_bf16_amx_extra(config, m, n, k, alpha, num_threads, **kwargs):
    # We need avx512_bf16 to dequant int8 to bf16
    vec_isa = kwargs.get("vec_isa")
    assert vec_isa is not None
    return vec_isa.is_avx512_bf16_supported() and check_amx_extra(
        config, m, n, k, alpha, num_threads, **kwargs
    )

