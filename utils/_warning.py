
def _warning(s):
    warnings.warn(f'scipy.cluster: {s}', ClusterWarning, stacklevel=3)

