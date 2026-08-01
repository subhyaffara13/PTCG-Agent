
def _dt_from_prefix(prefix):
    """Array dtype from a blas-style prefix."""
    if prefix.startswith('i'):
        prefix = prefix[1:]   # isamax, idamax etc
    elif prefix in ['sc', 'dz']:
        prefix = prefix[0]   # scasum, dzasum
    elif prefix in ['cs', 'zd']:
        prefix = prefix[0]  # zdscal, csscal

    dt_map = {'z': np.complex128, 'c': np.complex64, 'd': np.float64, 's': np.float32}
    return dt_map[prefix]

