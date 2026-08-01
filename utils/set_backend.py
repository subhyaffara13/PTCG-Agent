
def set_backend(name: Literal["NVSHMEM", "CUDA", "NCCL"]) -> None:
    r"""
    Set the backend for symmetric memory allocation. This is a global setting
    and affects all subsequent calls to
    :func:`torch._distributed._symmetric_memory.empty()`.  Note that the backend
    cannot be changed once a symmetric memory tensor has been allocated.

    Args:
        backend (str): the backend for symmetric memory allocation. Currently,
            only `"NVSHMEM"`, `"CUDA"`, `"NCCL"` are supported.
    """
    _SymmetricMemory.set_backend(name)


def set_backend(backend, coerce=False, only=False):
    """Context manager to set the backend within a fixed scope.

    Upon entering the ``with`` statement, the given backend will be added to
    the list of available backends with the highest priority. Upon exit, the
    backend is reset to the state before entering the scope.

    Parameters
    ----------
    backend : {object, 'scipy'}
        The backend to use.
        Can either be a ``str`` containing the name of a known backend
        {'scipy'} or an object that implements the uarray protocol.
    coerce : bool, optional
        Whether to allow expensive conversions for the ``x`` parameter. e.g.,
        copying a NumPy array to the GPU for a CuPy backend. Implies ``only``.
    only : bool, optional
        If only is ``True`` and this backend returns ``NotImplemented``, then a
        BackendNotImplemented error will be raised immediately. Ignoring any
        lower priority backends.

    Returns
    -------
    context : uarray._SetBackendContext
        Context manager that sets the backend.

    Examples
    --------
    >>> import scipy.fft as fft
    >>> with fft.set_backend('scipy', only=True):
    ...     fft.fft([1])  # Always calls the scipy implementation
    array([1.+0.j])
    """
    backend = _backend_from_arg(backend)
    return ua.set_backend(backend, coerce=coerce, only=only)


def set_backend(backend, coerce=False, only=False):
    """
    A context manager that sets the preferred backend.

    Parameters
    ----------
    backend
        The backend to set.
    coerce
        Whether or not to coerce to a specific backend's types. Implies ``only``.
    only
        Whether or not this should be the last backend to try.

    See Also
    --------
    skip_backend: A context manager that allows skipping of backends.
    set_global_backend: Set a single, global backend for a domain.
    """
    tid = threading.get_native_id()
    try:
        return backend.__ua_cache__[tid, "set", coerce, only]
    except AttributeError:
        backend.__ua_cache__ = {}
    except KeyError:
        pass

    ctx = _SetBackendContext(backend, coerce, only)
    backend.__ua_cache__[tid, "set", coerce, only] = ctx
    return ctx

