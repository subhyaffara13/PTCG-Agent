
def wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = get_running_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run


def wrap(fn_or_name: _F) -> _F: ...


def wrap(fn_or_name: str) -> str: ...


def wrap(fn_or_name: str | Callable[..., Any]) -> str | Callable[..., Any]:
    """
    This function can be called at module-level scope to register fn_or_name as a "leaf function".
    A "leaf function" will be preserved as a CallFunction node in the FX trace instead of being
    traced through::

        # foo/bar/baz.py
        def my_custom_function(x, y):
            return x * x + y * y


        torch.fx.wrap("my_custom_function")


        def fn_to_be_traced(x, y):
            # When symbolic tracing, the below call to my_custom_function will be inserted into
            # the graph rather than tracing it.
            return my_custom_function(x, y)

    This function can also equivalently be used as a decorator::

        # foo/bar/baz.py
        @torch.fx.wrap
        def my_custom_function(x, y):
            return x * x + y * y

    A wrapped function can be thought of a "leaf function", analogous to the concept of
    "leaf modules", that is, they are functions that are left as calls in the FX trace
    rather than traced through.

    Args:

        fn_or_name (Union[str, Callable]): The function or name of the global function to insert into the
            graph when it's called
    """
    if not callable(fn_or_name) and not isinstance(fn_or_name, str):
        raise RuntimeError(
            "Unsupported type for global function! Must be either a callable or "
            "string name"
        )

    if callable(fn_or_name):
        if isinstance(fn_or_name, str):  # to make mypy happy
            raise AssertionError("Unexpected: fn_or_name is both callable and str")
        fn_name = fn_or_name.__name__
    else:
        if not isinstance(fn_or_name, str):
            raise AssertionError(
                f"fn_or_name must be a global function or string name, got "
                f"{type(fn_or_name)}"
            )
        fn_name = fn_or_name

    currentframe = inspect.currentframe()
    if currentframe is None:
        raise AssertionError("inspect.currentframe() returned None")
    f = currentframe.f_back
    if f is None:
        raise AssertionError("currentframe.f_back is None")
    if f.f_code.co_name != "<module>":
        raise NotImplementedError("wrap must be called at the top level of a module")

    # consider implementing Callable version of this via _autowrap_function_ids / _autowrap_search
    # semantics would be slightly different, but would add support `from x import wrapped_function`
    _wrapped_fns_to_patch[(id(f.f_globals), fn_name)] = f.f_globals
    return fn_or_name


def wrap(arg, CCT, cct_mode):
    # CCT: CompositeCompliantTensor class which is generated using generate_cct_and_mode
    if isinstance(arg, torch.Tensor):
        return CCT(arg, cct_mode)
    if is_tensorlist(arg):
        return [CCT(a, cct_mode) for a in arg]
    raise RuntimeError("wrap assumes that the input can be wrapped")


def wrap(module: nn.Module, **wrap_overrides: Any) -> nn.Module:
    """
    Annotate that a module should be wrapped. Annotated modules will only be
    wrapped if inside of an :func:`enable_wrap` context manager. This allows
    a module to be initialized both with and without a wrapper without code
    change.

    The class that this function wraps the passed in ``nn.Module`` with is the
    passed in ``wrapper_cls`` argument into ``enable_wrap``. Both
    ``enable_wrap`` and ``wrap`` can take in kwargs specifying how to construct
    the ``wrapper_cls`` instance. In the case of duplicate kwargs in
    ``enable_wrap`` and ``wrap``, the argument passed into ``wrap`` will be
    respected.

    Usage::

        with enable_wrap(wrapper_cls=FSDP, **fsdp_config):
            # Wraps layer in FSDP by default if within context
            self.l1 = wrap(torch.nn.Linear(5, 5))

    Args:
        module (nn.Module): module to wrap (if in :func:`enable_wrap` context)
        **wrap_overrides: configuration overrides that will take priority over
            the values provided by the :func:`enable_wrap` context
    """
    if _ConfigAutoWrap.in_autowrap_context:
        if _ConfigAutoWrap.wrapper_cls is None:
            raise AssertionError("Expected _ConfigAutoWrap.wrapper_cls to be set")

        wrap_overrides = {**_ConfigAutoWrap.kwargs, **wrap_overrides}
        return _wrap(
            module,
            _ConfigAutoWrap.wrapper_cls,
            **wrap_overrides,
        )
    return module


def wrap(text, width=80):
    """Line wrap a polynomial expression. """
    out = ''
    col = 0
    for c in text:
        if c == ' ' and col > width:
            c, col = '\n', 0
        else:
            col += 1
        out += c
    return out


def wrap(s):
    """
    Wrap lines of text, retaining existing newlines as
    paragraph markers.

    >>> print(wrap(lorem_ipsum))
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
    eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
    minim veniam, quis nostrud exercitation ullamco laboris nisi ut
    aliquip ex ea commodo consequat. Duis aute irure dolor in
    reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
    pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
    culpa qui officia deserunt mollit anim id est laborum.
    <BLANKLINE>
    Curabitur pretium tincidunt lacus. Nulla gravida orci a odio. Nullam
    varius, turpis et commodo pharetra, est eros bibendum elit, nec luctus
    magna felis sollicitudin mauris. Integer in mauris eu nibh euismod
    gravida. Duis ac tellus et risus vulputate vehicula. Donec lobortis
    risus a elit. Etiam tempor. Ut ullamcorper, ligula eu tempor congue,
    eros est euismod turpis, id tincidunt sapien risus a quam. Maecenas
    fermentum consequat mi. Donec fermentum. Pellentesque malesuada nulla
    a mi. Duis sapien sem, aliquet nec, commodo eget, consequat quis,
    neque. Aliquam faucibus, elit ut dictum aliquet, felis nisl adipiscing
    sapien, sed malesuada diam lacus eget erat. Cras mollis scelerisque
    nunc. Nullam arcu. Aliquam consequat. Curabitur augue lorem, dapibus
    quis, laoreet et, pretium ac, nisi. Aenean magna nisl, mollis quis,
    molestie eu, feugiat in, orci. In hac habitasse platea dictumst.
    """
    paragraphs = s.splitlines()
    wrapped = ('\n'.join(textwrap.wrap(para)) for para in paragraphs)
    return '\n\n'.join(wrapped)


def wrap(path):  # pragma: no cover
    """
    Workaround for https://github.com/python/cpython/issues/84538
    to add backward compatibility for walk_up=True.
    An example affected package is dask-labextension, which uses
    jupyter-packaging to install JupyterLab javascript files outside
    of site-packages.
    """

    def relative_to(root, *, walk_up=False):
        return pathlib.Path(os.path.relpath(path, root))

    return types.SimpleNamespace(relative_to=relative_to)


def wrap(message: List[str]) -> List[str]:
  """Given a list of strings, returns a list of them `wrapped` (paragraphs).

  Args:
    message: list of strings
  Returns:
    wrapped: list of strings with each string `wrapped` so that each line only
      contains (default) 70 characters
  """
  wrapped = []
  for sub_msg in message:
    sub_msg_wrapped = textwrap.wrap(sub_msg)
    if len(sub_msg_wrapped) > 1:
      sub_msg_wrapped = ['\n'.join(sub_msg_wrapped)]
    wrapped.extend(sub_msg_wrapped)
  return wrapped


def wrap(path):  # pragma: no cover
    """
    Workaround for https://github.com/python/cpython/issues/84538
    to add backward compatibility for walk_up=True.
    An example affected package is dask-labextension, which uses
    jupyter-packaging to install JupyterLab javascript files outside
    of site-packages.
    """

    def relative_to(root, *, walk_up=False):
        return pathlib.Path(os.path.relpath(path, root))

    return types.SimpleNamespace(relative_to=relative_to)


def wrap(x: float, m: float, big_m: float) -> jnp.ndarray:
    """For example, m = -180, M = 180 (degrees), x = 360 --> returns 0."""
    diff = big_m - m
    go_up = x < m  # Wrap if x is outside the left bound
    go_down = x >= big_m  # Wrap if x is outside OR on the right bound

    how_often = go_up * jnp.ceil(
        (m - x) / diff
    ) + go_down * jnp.floor(  # if m - x is an integer, keep it
        (x - big_m) / diff + 1
    )  # if x - M is an integer, round up
    x_out = x - how_often * diff * go_down + how_often * diff * go_up
    return x_out


def wrap(x, m, M):
    """Wraps `x` so m <= x <= M; but unlike `bound()` which
    truncates, `wrap()` wraps x around the coordinate system defined by m,M.\n
    For example, m = -180, M = 180 (degrees), x = 360 --> returns 0.

    Args:
        x: a scalar
        m: minimum possible value in range
        M: maximum possible value in range

    Returns:
        x: a scalar, wrapped
    """
    diff = M - m
    while x > M:
        x = x - diff
    while x < m:
        x = x + diff
    return x


def wrap(x, m, M):
    """Wraps ``x`` so m <= x <= M; but unlike ``bound()`` which
    truncates, ``wrap()`` wraps x around the coordinate system defined by m,M.\n
    For example, m = -180, M = 180 (degrees), x = 360 --> returns 0.

    Args:
        x: a scalar
        m: minimum possible value in range
        M: maximum possible value in range

    Returns:
        x: a scalar, wrapped
    """
    diff = M - m
    while x > M:
        x = x - diff
    while x < m:
        x = x + diff
    return x


def wrap(base_io_obj, file, *, loop=None, executor=None):
    """Wrap the object with interface based on type of underlying IO"""

    msg = f"Unsupported IO type: {base_io_obj}"
    raise TypeError(msg)


def wrap(file, *, loop=None, executor=None):
    msg = f"Unsupported io type: {file}."
    raise TypeError(msg)

