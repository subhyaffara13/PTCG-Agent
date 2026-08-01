
def check_brgemm_extra(config, m, n, k, alpha, num_threads, **kwargs):
    assert config.input_dtype == torch.half and config.output_dtype == torch.float
    vnni_size = 2
    # use brgemm for Half when amx_fp16 is supported
    return torch.cpu._is_amx_fp16_supported() and k % vnni_size == 0 and alpha == 1

