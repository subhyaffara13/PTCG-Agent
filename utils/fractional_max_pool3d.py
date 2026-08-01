
def fractional_max_pool3d(x, kernel_size, output_size, random_samples):
    return _fractional_max_pool(x, kernel_size, output_size, random_samples, n_dim=3)

