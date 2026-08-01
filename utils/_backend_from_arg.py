
def _backend_from_arg(backend):
    """Maps strings to known backends and validates the backend"""

    if isinstance(backend, str):
        try:
            backend = _named_backends[backend]
        except KeyError as e:
            raise ValueError(f'Unknown backend {backend}') from e

    if backend.__ua_domain__ != 'numpy.scipy.fft':
        raise ValueError('Backend does not implement "numpy.scipy.fft"')

    return backend

