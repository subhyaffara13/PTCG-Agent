
def _gen_gaussians_even(sigmas, total_length):
    num_peaks = len(sigmas)
    delta = total_length / (num_peaks + 1)
    center_locs = np.linspace(delta, total_length - delta, num=num_peaks).astype(int)
    out_data = _gen_gaussians(center_locs, sigmas, total_length)
    return out_data, center_locs

