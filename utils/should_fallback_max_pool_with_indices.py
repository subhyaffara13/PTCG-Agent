
def should_fallback_max_pool_with_indices(kernel_size, *, n_dim):
    kernel_size = pad_listlike(kernel_size, n_dim)
    window_size = functools.reduce(operator.mul, kernel_size)
    return window_size > 25

