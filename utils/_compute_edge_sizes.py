
def _compute_edge_sizes(n_fft, window_size):
    """Helper function to compute the sizes of the edges (left and right)
    of a given window centered within an FFT size."""
    left = (n_fft - window_size) // 2
    right = n_fft - left - window_size
    return left, right

