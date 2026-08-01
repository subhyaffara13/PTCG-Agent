
def skip_backend(backend):
    """Context manager to skip a backend within a fixed scope.

    Within the context of a ``with`` statement, the given backend will not be
    called. This covers backends registered both locally and globally. Upon
    exit, the backend will again be considered.

    Parameters
    ----------
    backend : {object, 'scipy'}
        The backend to skip.
        Can either be a ``str`` containing the name of a known backend
        {'scipy'} or an object that implements the uarray protocol.

    Returns
    -------
    context : uarray._SetBackendContext
        Context manager that skips the backend.

    Examples
    --------
    >>> import scipy.fft as fft
    >>> fft.fft([1])  # Calls default SciPy backend
    array([1.+0.j])
    >>> with fft.skip_backend('scipy'):  # We explicitly skip the SciPy backend
    ...     fft.fft([1])                 # leaving no implementation available
    Traceback (most recent call last):
        ...
    BackendNotImplementedError: No selected backends had an implementation ...
    """
    backend = _backend_from_arg(backend)
    return ua.skip_backend(backend)


def skip_backend(backend):
    """
    A context manager that allows one to skip a given backend from processing
    entirely. This allows one to use another backend's code in a library that
    is also a consumer of the same backend.

    Parameters
    ----------
    backend
        The backend to skip.

    See Also
    --------
    set_backend: A context manager that allows setting of backends.
    set_global_backend: Set a single, global backend for a domain.
    """
    tid = threading.get_native_id()
    try:
        return backend.__ua_cache__[tid, "skip"]
    except AttributeError:
        backend.__ua_cache__ = {}
    except KeyError:
        pass

    ctx = _SkipBackendContext(backend)
    backend.__ua_cache__[tid, "skip"] = ctx
    return ctx

