
def register_backend(format, backend, description=None):
    """
    Register a backend for saving to a given file format.

    Parameters
    ----------
    format : str
        File extension
    backend : module string or canvas class
        Backend for handling file output
    description : str, default: ""
        Description of the file type.
    """
    if description is None:
        description = ''
    _default_backends[format] = backend
    _default_filetypes[format] = description


def register_backend(name: str, func: ProcessGroupFactory) -> None:
    """
    Register a new process group backend.

    Args:
        name: The name of the backend.
        func: The function to create the process group.
    """
    if name in _BACKENDS:
        raise ValueError(f"Backend {name} already registered")

    _BACKENDS[name] = func


def register_backend(
    compiler_fn: CompilerFn | None = None,
    name: str | None = None,
    tags: Sequence[str] = (),
) -> Callable[..., Any]:
    """
    Decorator to add a given compiler to the registry to allow calling
    `torch.compile` with string shorthand.  Note: for projects not
    imported by default, it might be easier to pass a function directly
    as a backend and not use a string.

    Args:
        compiler_fn: Callable taking a FX graph and fake tensor inputs
        name: Optional name, defaults to `compiler_fn.__name__`
        tags: Optional set of string tags to categorize backend with
    """
    if compiler_fn is None:
        # @register_backend(name="") syntax
        return functools.partial(register_backend, name=name, tags=tags)  # type: ignore[return-value]
    assert callable(compiler_fn)
    name = name or compiler_fn.__name__
    assert name not in _COMPILER_FNS, f"duplicate name: {name}"
    if compiler_fn not in _BACKENDS:
        _BACKENDS[name] = None
    _COMPILER_FNS[name] = compiler_fn
    compiler_fn._tags = tuple(tags)  # type: ignore[attr-defined]
    return compiler_fn


def register_backend(
    backend_name, construct_rpc_backend_options_handler, init_backend_handler
):
    """Registers a new RPC backend.

    Args:
        backend_name (str): backend string to identify the handler.
        construct_rpc_backend_options_handler (function):
            Handler that is invoked when
            rpc_backend.construct_rpc_backend_options(**dict) is called.
        init_backend_handler (function): Handler that is invoked when the
            `_init_rpc_backend()` function is called with a backend.
             This returns the agent.
    """
    global BackendType
    if backend_registered(backend_name):
        raise RuntimeError(f"RPC backend {backend_name}: already registered")
    # Create a new enum type, `BackendType`, with extended members.
    existing_enum_dict = {member.name: member.value for member in BackendType}
    extended_enum_dict = dict(
        {
            backend_name: BackendValue(
                construct_rpc_backend_options_handler=construct_rpc_backend_options_handler,
                init_backend_handler=init_backend_handler,
            )
        },
        **existing_enum_dict,
    )
    # Can't handle Function Enum API (mypy bug #9079)
    BackendType = enum.Enum(value="BackendType", names=extended_enum_dict)  # type: ignore[misc]
    # Unable to assign a function a method (mypy bug #2427)
    BackendType.__repr__ = _backend_type_repr  # type: ignore[assignment]
    if BackendType.__doc__:
        BackendType.__doc__ = _backend_type_doc

    return BackendType[backend_name]


def register_backend(backend):
    """
    Register a backend for permanent use.

    Registered backends have the lowest priority and will be tried after the
    global backend.

    Parameters
    ----------
    backend : {object, 'scipy'}
        The backend to use.
        Can either be a ``str`` containing the name of a known backend
        {'scipy'} or an object that implements the uarray protocol.

    Raises
    ------
    ValueError: If the backend does not implement ``numpy.scipy.fft``.

    Examples
    --------
    We can register a new fft backend:

    >>> from scipy.fft import fft, register_backend, set_global_backend
    >>> class NoopBackend:  # Define an invalid Backend
    ...     __ua_domain__ = "numpy.scipy.fft"
    ...     def __ua_function__(self, func, args, kwargs):
    ...          return NotImplemented
    >>> set_global_backend(NoopBackend())  # Set the invalid backend as global
    >>> register_backend("scipy")  # Register a new backend
    # The registered backend is called because
    # the global backend returns `NotImplemented`
    >>> fft([1])
    array([1.+0.j])
    >>> set_global_backend("scipy")  # Restore global backend to default

    """
    backend = _backend_from_arg(backend)
    ua.register_backend(backend)


def register_backend(backend):
    """
    This utility method sets registers backend for permanent use. It
    will be tried in the list of backends automatically, unless the
    ``only`` flag is set on a backend.

    Note that this method is not thread-safe.

    Parameters
    ----------
    backend
        The backend to register.
    """
    _uarray.register_backend(backend)

