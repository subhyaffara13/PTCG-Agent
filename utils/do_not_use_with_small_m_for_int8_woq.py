
def do_not_use_with_small_m_for_int8_woq(config, m, n, k, alpha, num_threads, **kwargs):
    return not check_int8_woq_small_m_dim(config, m, n, k, alpha, num_threads, **kwargs)

