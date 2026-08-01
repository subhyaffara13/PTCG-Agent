
def winsor_reference_1d(y, p, method):
    # Adapted directly from the documentation
    # Note: `y` is the sorted data array
    n = len(y)
    if method == 'round_nearest':
        j = int(np.round(p * n) if p < 0.5 else np.round(n * p - 1))
    elif method == 'round_outward':
        j = int(np.floor(p * n) if p < 0.5 else np.ceil(n * p - 1))
    elif method == 'round_inward':
        j = int(np.ceil(p * n) if p < 0.5 else np.floor(n * p - 1))
    return y[j]

