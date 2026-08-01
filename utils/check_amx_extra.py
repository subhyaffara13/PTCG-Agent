
def check_amx_extra(config, m, n, k, alpha, num_threads, **kwargs):
    vnni_size = 4 if config.input_dtype in [torch.uint8, torch.int8] else 2
    return k % vnni_size == 0 and alpha == 1

