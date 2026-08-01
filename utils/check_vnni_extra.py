
def check_vnni_extra(config, m, n, k, alpha, num_threads, **kwargs):
    assert config.input_dtype == torch.uint8 and config.input2_dtype == torch.int8
    vnni_size = 4
    return k % vnni_size == 0

