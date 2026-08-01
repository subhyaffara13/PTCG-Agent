
def check_amx_fp16_extra(config, m, n, k, alpha, num_threads, **kwargs):
    assert config.input_dtype == torch.float16 and config.output_dtype == torch.float
    vec_isa = kwargs.get("vec_isa")
    assert vec_isa is not None
    vnni_size = 2
    return vec_isa.is_amx_fp16_supported() and k % vnni_size == 0 and alpha == 1

