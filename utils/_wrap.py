
def _wrap(f):
    """ encapsulate a function and it's __import__ """
    def func(*args, **kwds):
        try:
            # _ = eval(getsource(f, force=True)) #XXX: safer but less robust
            exec(getimportable(f, alias='_'), __globals__, __locals__)
        except Exception:
            raise ImportError('cannot import name ' + f.__name__)
        return _(*args, **kwds)
    func.__name__ = f.__name__
    func.__doc__ = f.__doc__
    return func


def _wrap(fn, i, args, error_file):
    # prctl(2) is a Linux specific system call.
    # On other systems the following function call has no effect.
    # This is set to ensure that non-daemonic child processes can
    # terminate if their parent terminates before they do.
    _prctl_pr_set_pdeathsig(signal.SIGINT)

    try:
        fn(i, *args)
    except KeyboardInterrupt:
        pass  # SIGINT; Killed by parent, do nothing
    except Exception:
        # Propagate exception to parent process, keeping original traceback
        import traceback

        with open(error_file, "wb") as fh:
            pickle.dump(traceback.format_exc(), fh)
        sys.exit(1)


def _wrap(module: nn.Module, wrapper_cls: Callable, **kwargs) -> nn.Module:
    if wrapper_cls is None:
        raise AssertionError("Expected wrapper_cls to be set")
    if hasattr(module, "_wrap_overrides"):
        # If module has a _wrap_overrides attribute, we force overriding the
        # FSDP config with these attributes for this module. Currently this
        # is only used to disable mixed precision for BatchNorm when
        # auto_wrapping.
        overrides = {**kwargs, **module._wrap_overrides}  # type: ignore[arg-type, dict-item]
        return wrapper_cls(module, **overrides)

    return wrapper_cls(module, **kwargs)


def _wrap(
    local_rank: int,
    fn: Callable,
    args: dict[int, tuple],
    envs: dict[int, dict[str, str]],
    stdout_redirects: dict[int, str],  # redirect file for stdout (to console if None)
    stderr_redirects: dict[int, str],  # redirect file for stderr (to console if None)
    ret_vals: dict[int, mp.SimpleQueue],
    queue_finished_reading_event: synchronize.Event,
    numa_options: NumaOptions | None,
) -> None:
    # get the per-rank params up front so we fail fast if no mapping is found
    args_ = args[local_rank]
    env_ = envs[local_rank]
    ret_val_ = ret_vals[local_rank]

    stdout_rd = stdout_redirects[local_rank]
    stderr_rd = stderr_redirects[local_rank]

    stdout_cm = get_std_cm(stdout_rd, redirect_stdout)
    stderr_cm = get_std_cm(stderr_rd, redirect_stderr)

    for k, v in env_.items():
        os.environ[k] = v

    with stdout_cm, stderr_cm:
        fn = _maybe_wrap_with_numa_binding(
            fn, gpu_index=local_rank, numa_options=numa_options
        )
        ret = record(fn)(*args_)
    ret_val_.put(ret)
    queue_finished_reading_event.wait()


def _wrap(
    orig: Callable,
    dim_offset: int | None = None,
    keepdim_offset: int | None = None,
    dim_name: str | None = None,
    single_dim: bool | None = None,
    reduce: bool | None = None,
) -> Callable:
    """
    Wrap a PyTorch function to support first-class dimensions.

    Args:
        orig: Original function to wrap
        dim_offset: Offset for dimension argument (default: 0)
        keepdim_offset: Offset for keepdim argument (default: 1)
        dim_name: Name of dimension parameter (default: "dim")
        single_dim: Whether function takes single dimension (default: False)
        reduce: Whether function reduces dimensions (default: True)
    """
    dim_name = dim_name or "dim"

    wrapper = WrappedOperator(orig, patched_dim_method, dim_name)

    if dim_offset is not None:
        wrapper.dim_offset = dim_offset
    if keepdim_offset is not None:
        wrapper.keepdim_offset = keepdim_offset
    if single_dim is not None:
        wrapper.single_dim = single_dim
    if reduce is not None:
        wrapper.reduce = reduce

    return wrapper.function()


def _wrap(
    flag_overrider_cls: type['_FlagOverrider'],
    func: _CallableT,
    overrides: Mapping[str, Any],
) -> _CallableT:
  ...


def _wrap(
    flag_overrider_cls: type['_ParsingFlagOverrider'],
    func: _CallableT,
    overrides: Mapping[str, str | Sequence[str]],
) -> _CallableT:
  ...


def _wrap(flag_overrider_cls, func, overrides):
  """Creates a wrapper function that saves/restores flag values.

  Args:
    flag_overrider_cls: The class that will be used as a context manager.
    func: This will be called between saving flags and restoring flags.
    overrides: Flag names mapped to their values. These flags will be set after
      saving the original flag state. The type of the values depends on if
      _FlagOverrider or _ParsingFlagOverrider was specified.

  Returns:
    A wrapped version of func.
  """

  @functools.wraps(func)
  def _flagsaver_wrapper(*args, **kwargs):
    """Wrapper function that saves and restores flags."""
    with flag_overrider_cls(**overrides):
      return func(*args, **kwargs)

  return _flagsaver_wrapper

