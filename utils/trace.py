import logging
import os
import sys
from typing import Any, Optional, Union

def trace(arg: Union[bool, TextIO, str, os.PathLike] = None, *, mode: str = 'a') -> None:
    """print a trace through the stack when pickling; useful for debugging

    With a single boolean argument, enable or disable the tracing.

    Example usage:

        >>> import dill
        >>> dill.detect.trace(True)
        >>> dill.dump_session()

    Alternatively, ``trace()`` can be used as a context manager. With no
    arguments, it just takes care of restoring the tracing state on exit.
    Either a file handle, or a file name and (optionally) a file mode may be
    specitfied to redirect the tracing output in the ``with`` block context. A
    log function is yielded by the manager so the user can write extra
    information to the file.

    Example usage:

        >>> from dill import detect
        >>> D = {'a': 42, 'b': {'x': None}}
        >>> with detect.trace():
        >>>     dumps(D)
        ┬ D2: <dict object at 0x7f2721804800>
        ├┬ D2: <dict object at 0x7f27217f5c40>
        │└ # D2 [8 B]
        └ # D2 [22 B]
        >>> squared = lambda x: x**2
        >>> with detect.trace('output.txt', mode='w') as log:
        >>>     log("> D = %r", D)
        >>>     dumps(D)
        >>>     log("> squared = %r", squared)
        >>>     dumps(squared)

    Arguments:
        arg: a boolean value, or an optional file-like or path-like object for the context manager
        mode: mode string for ``open()`` if a file name is passed as the first argument
    """
    if repr(arg) not in ('False', 'True'):
        return TraceManager(file=arg, mode=mode)
    logger.setLevel(logging.INFO if arg else logging.WARNING)


def trace(
    name: str, info: typing.Mapping[str, typing.Any], verbose: bool = False
) -> None:
    console = rich.console.Console()
    if name == "connection.connect_tcp.started" and verbose:
        host = info["host"]
        console.print(f"* Connecting to {host!r}")
    elif name == "connection.connect_tcp.complete" and verbose:
        stream = info["return_value"]
        server_addr = stream.get_extra_info("server_addr")
        console.print(f"* Connected to {server_addr[0]!r} on port {server_addr[1]}")
    elif name == "connection.start_tls.complete" and verbose:  # pragma: no cover
        stream = info["return_value"]
        ssl_object = stream.get_extra_info("ssl_object")
        version = ssl_object.version()
        cipher = ssl_object.cipher()
        server_cert = ssl_object.getpeercert()
        alpn = ssl_object.selected_alpn_protocol()
        console.print(f"* SSL established using {version!r} / {cipher[0]!r}")
        console.print(f"* Selected ALPN protocol: {alpn!r}")
        if server_cert:
            console.print("* Server certificate:")
            console.print(format_certificate(server_cert))
    elif name == "http11.send_request_headers.started" and verbose:
        request = info["request"]
        print_request_headers(request, http2=False)
    elif name == "http2.send_request_headers.started" and verbose:  # pragma: no cover
        request = info["request"]
        print_request_headers(request, http2=True)
    elif name == "http11.receive_response_headers.complete":
        http_version, status, reason_phrase, headers = info["return_value"]
        print_response_headers(http_version, status, reason_phrase, headers)
    elif name == "http2.receive_response_headers.complete":  # pragma: no cover
        status, headers = info["return_value"]
        http_version = b"HTTP/2"
        reason_phrase = None
        print_response_headers(http_version, status, reason_phrase, headers)


def trace(data):
    out = io.StringIO()

    def format(entries):
        segment_intervals: list = []
        segment_addr_to_name = {}
        allocation_addr_to_name = {}

        free_names: list = []
        next_name = 0

        def _name():
            nonlocal next_name
            if free_names:
                return free_names.pop()
            r, m = next_name // 26, next_name % 26
            next_name += 1
            return f"{chr(ord('a') + m)}{'' if r == 0 else r}"

        def find_segment(addr):
            for name, saddr, size in segment_intervals:
                if addr >= saddr and addr < saddr + size:
                    return name, saddr
            for i, seg in enumerate(data["segments"]):
                saddr = seg["address"]
                size = seg["allocated_size"]
                if addr >= saddr and addr < saddr + size:
                    return f"seg_{i}", saddr
            return None, None

        count = 0
        out.write(f"{len(entries)} entries\n")

        total_reserved = 0
        for seg in data["segments"]:
            total_reserved += seg["total_size"]

        for count, e in enumerate(entries):
            if e["action"] == "alloc":
                addr, size = e["addr"], e["size"]
                n = _name()
                seg_name, seg_addr = find_segment(addr)
                if seg_name is None:
                    seg_name = "MEM"
                    offset = addr
                else:
                    offset = addr - seg_addr
                out.write(f"{n} = {seg_name}[{offset}:{Bytes(size)}]\n")
                allocation_addr_to_name[addr] = (n, size, count)
                count += size
            elif e["action"] == "free_requested":
                addr, size = e["addr"], e["size"]
                name, _, _ = allocation_addr_to_name.get(addr, (addr, None, None))
                out.write(f"del {name} # {Bytes(size)}\n")
            elif e["action"] == "free_completed":
                addr, size = e["addr"], e["size"]
                count -= size
                name, _, _ = allocation_addr_to_name.get(addr, (addr, None, None))
                out.write(f"# free completed for {name} {Bytes(size)}\n")
                if name in allocation_addr_to_name:
                    free_names.append(name)
                    del allocation_addr_to_name[name]
            elif e["action"] == "segment_alloc":
                addr, size = e["addr"], e["size"]
                name = _name()
                out.write(f"{name} = cudaMalloc({addr}, {Bytes(size)})\n")
                segment_intervals.append((name, addr, size))
                segment_addr_to_name[addr] = name
            elif e["action"] == "segment_free":
                addr, size = e["addr"], e["size"]
                name = segment_addr_to_name.get(addr, addr)
                out.write(f"cudaFree({name}) # {Bytes(size)}\n")
                if name in segment_addr_to_name:
                    free_names.append(name)
                    del segment_addr_to_name[name]
            elif e["action"] == "oom":
                size = e["size"]
                free = e["device_free"]
                out.write(
                    f"raise OutOfMemoryError # {Bytes(size)} requested, {Bytes(free)} free in CUDA\n"
                )
            else:
                out.write(f"{e}\n")
        out.write(f"TOTAL MEM: {Bytes(count)}")

    for i, d in enumerate(data["device_traces"]):
        if d:
            out.write(f"Device {i} ----------------\n")
            format(d)
    return out.getvalue()


def trace(
    func,
    example_inputs=None,
    optimize=None,
    check_trace=True,
    check_inputs=None,
    check_tolerance=1e-5,
    strict=True,
    _force_outplace=False,
    _module_class=None,
    _compilation_unit=_python_cu,
    example_kwarg_inputs=None,
    _store_inputs=True,
):
    r"""
    Trace a function and return an executable  or :class:`ScriptFunction` that will be optimized using just-in-time compilation.

    Tracing is ideal for code that operates only on
    ``Tensor``\\s and lists, dictionaries, and
    tuples of ``Tensor``\\s.

    Using `torch.jit.trace` and `torch.jit.trace_module`, you can turn an
    existing module or Python function into a TorchScript
    :class:`ScriptFunction` or :class:`ScriptModule`. You must provide example
    inputs, and we run the function, recording the operations performed on all
    the tensors.

    * The resulting recording of a standalone function produces `ScriptFunction`.
    * The resulting recording of `nn.Module.forward` or `nn.Module` produces
      `ScriptModule`.

    This module also contains any parameters that the original
    module had as well.

    Warning:
        Tracing only correctly records functions and modules which are not data
        dependent (e.g., do not have conditionals on data in tensors) and do not have
        any untracked external dependencies (e.g., perform input/output or
        access global variables). Tracing only records operations done when the given
        function is run on the given tensors. Therefore, the returned
        `ScriptModule` will always run the same traced graph on any input. This
        has some important implications when your module is expected to run
        different sets of operations, depending on the input and/or the module
        state. For example,

        * Tracing will not record any control-flow like if-statements or loops.
          When this control-flow is constant across your module, this is fine
          and it often inlines the control-flow decisions. But sometimes the
          control-flow is actually part of the model itself. For instance, a
          recurrent network is a loop over the (possibly dynamic) length of an
          input sequence.
        * In the returned :class:`ScriptModule`, operations that have different
          behaviors in ``training`` and ``eval`` modes will always behave as if
          it is in the mode it was in during tracing, no matter which mode the
          `ScriptModule` is in.

        In cases like these, tracing would not be appropriate and
        :func:`scripting <torch.jit.script>` is a better choice. If you trace
        such models, you may silently get incorrect results on subsequent
        invocations of the model. The tracer will try to emit warnings when
        doing something that may cause an incorrect trace to be produced.

    Args:
        func (callable or torch.nn.Module):  A Python function or `torch.nn.Module`
            that will be run with `example_inputs`. `func` arguments and return
            values  must be tensors or (possibly nested) tuples that contain
            tensors. When a module is passed `torch.jit.trace`, only the
            ``forward`` method is run and traced (see :func:`torch.jit.trace
            <torch.jit.trace_module>` for details).

    Keyword arguments:
        example_inputs (tuple or torch.Tensor or None, optional): A tuple of example
            inputs that will be passed to the function while tracing.
            Default: ``None``. Either this argument or ``example_kwarg_inputs``
            should be specified. The resulting trace can be run with inputs of
            different types and shapes assuming the traced operations support those
            types and shapes. `example_inputs` may also be a single Tensor in which
            case it is automatically wrapped in a tuple. When the value is None,
            ``example_kwarg_inputs`` should be specified.

        check_trace (``bool``, optional): Check if the same inputs run through
            traced code produce the same outputs. Default: ``True``. You might want
            to disable this if, for example, your network contains non-
            deterministic ops or if you are sure that the network is correct despite
            a checker failure.

        check_inputs (list of tuples, optional): A list of tuples of input
            arguments that should be used to check the trace against what is
            expected. Each tuple is equivalent to a set of input arguments that
            would be specified in ``example_inputs``. For best results, pass in
            a set of checking inputs representative of the space of shapes and
            types of inputs you expect the network to see.  If not specified,
            the original ``example_inputs`` are used for checking
        check_tolerance (float, optional): Floating-point comparison tolerance
            to use in the checker procedure.  This can be used to relax the
            checker strictness in the event that results diverge numerically
            for a known reason, such as operator fusion.
        strict (``bool``, optional): run the tracer in a strict mode or not
            (default: ``True``). Only turn this off when you want the tracer to
            record your mutable container types (currently ``list``/``dict``)
            and you are sure that the container you are using in your
            problem is a ``constant`` structure and does not get used as
            control flow (if, for) conditions.
        example_kwarg_inputs (dict, optional): This parameter is a pack of keyword
            arguments of example inputs that will be passed to the function while
            tracing. Default: ``None``. Either this argument or ``example_inputs``
            should be specified. The dict will be unpacking by the arguments name
            of the traced function. If the keys of the dict don't not match with
            the traced function's arguments name, a runtime exception will be raised.

    Returns:
        If `func` is `nn.Module` or ``forward`` of `nn.Module`, `trace` returns
        a :class:`ScriptModule` object with a single ``forward`` method
        containing the traced code.  The returned `ScriptModule` will
        have the same set of sub-modules and parameters as the original
        ``nn.Module``.  If ``func`` is a standalone function, ``trace``
        returns `ScriptFunction`.

    Example (tracing a function):

    .. testcode::

        import torch

        def foo(x, y):
            return 2 * x + y

        # Run `foo` with the provided inputs and record the tensor operations
        traced_foo = torch.jit.trace(foo, (torch.rand(3), torch.rand(3)))

        # `traced_foo` can now be run with the TorchScript interpreter or saved
        # and loaded in a Python-free environment

    Example (tracing an existing module)::

        import torch
        import torch.nn as nn


        class Net(nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.conv = nn.Conv2d(1, 1, 3)

            def forward(self, x):
                return self.conv(x)


        n = Net()
        example_weight = torch.rand(1, 1, 3, 3)
        example_forward_input = torch.rand(1, 1, 3, 3)

        # Trace a specific method and construct `ScriptModule` with
        # a single `forward` method
        module = torch.jit.trace(n.forward, example_forward_input)

        # Trace a module (implicitly traces `forward`) and construct a
        # `ScriptModule` with a single `forward` method
        module = torch.jit.trace(n, example_forward_input)

    """
    if sys.version_info >= (3, 14):
        warnings.warn(
            "`torch.jit.trace` is not supported in Python 3.14+ and may break. "
            "Please switch to `torch.compile` or `torch.export`.",
            DeprecationWarning,
        )
    else:
        warnings.warn(
            "`torch.jit.trace` is deprecated. Please switch to `torch.compile` or `torch.export`.",
            DeprecationWarning,
        )
    if not _enabled:
        return func
    if optimize is not None:
        warnings.warn(
            "`optimize` is deprecated and has no effect. "
            "Use `with torch.jit.optimized_execution()` instead",
            FutureWarning,
            stacklevel=2,
        )

    from torch._utils_internal import log_torchscript_usage

    traced_func = _trace_impl(
        func,
        example_inputs,
        optimize,
        check_trace,
        check_inputs,
        check_tolerance,
        strict,
        _force_outplace,
        _module_class,
        _compilation_unit,
        example_kwarg_inputs,
        _store_inputs,
    )
    log_torchscript_usage("trace", model_id=_get_model_id(traced_func))
    return traced_func


def trace(self: Tensor) -> Tensor:
    return torch.sum(torch.diag(self))


def trace(
    a: ArrayLike,
    offset=0,
    axis1=0,
    axis2=1,
    dtype: DTypeLike | None = None,
    out: OutArray | None = None,
):
    result = torch.diagonal(a, offset, dim1=axis1, dim2=axis2).sum(-1, dtype=dtype)
    return result


def trace(self: TensorLikeType) -> TensorLikeType:
    torch._check(
        self.ndim == 2,
        lambda: f"expected a matrix, but got tensor with dim {self.ndim}",
    )
    return torch.sum(torch.diag(self, 0))


def trace(expr):
    """Trace of a Matrix.  Sum of the diagonal elements.

    Examples
    ========

    >>> from sympy import trace, Symbol, MatrixSymbol, eye
    >>> n = Symbol('n')
    >>> X = MatrixSymbol('X', n, n)  # A square matrix
    >>> trace(2*X)
    2*Trace(X)
    >>> trace(eye(3))
    3
    """
    return Trace(expr).doit()


def trace(
    x: Array,
    /,
    xp: Namespace,
    *,
    offset: int = 0,
    dtype: DType | None = None,
    **kwargs: object,
) -> Array:
    return xp.asarray(
        xp.trace(x, offset=offset, dtype=dtype, axis1=-2, axis2=-1, **kwargs)
    )


def trace(x: Array, /, *, offset: int = 0, dtype: DType | None = None) -> Array:
    # Use our wrapped sum to make sure it does upcasting correctly
    return sum(torch.diagonal(x, offset=offset, dim1=-2, dim2=-1), axis=-1, dtype=dtype)


def trace(
    decay: jax.typing.ArrayLike,
    nesterov: bool = False,
    accumulator_dtype: Optional[Any] = None,
) -> base.GradientTransformation:
  """Compute a trace of past updates.

  Args:
    decay: Decay rate for the trace of past updates.
    nesterov: Whether to use Nesterov momentum.
    accumulator_dtype: Optional `dtype` to be used for the accumulator; if
      `None` then the `dtype` is inferred from `params` and `updates`.

  Returns:
    A :class:`optax.GradientTransformation` object.

  .. note::
    :func:`optax.trace` and :func:`optax.ema` have very similar but distinct
    updates; ``trace = decay * trace + t``, while
    ``ema = decay * ema + (1-decay) * t``.
    Both are frequently found in the optimization literature.
  """

  accumulator_dtype = utils.canonicalize_dtype(accumulator_dtype)

  def init_fn(params):
    return TraceState(
        trace=optax.tree.zeros_like(params, dtype=accumulator_dtype)
    )

  def update_fn(updates, state, params=None):
    del params
    f = lambda g, t: g + decay * t
    new_trace = jax.tree.map(
        lambda g, t: None if g is None else f(g, t),
        updates,
        state.trace,
        is_leaf=lambda g: g is None,
    )
    updates = jax.tree.map(f, updates, new_trace) if nesterov else new_trace
    new_trace = optax.tree.cast(new_trace, accumulator_dtype)
    return updates, TraceState(trace=new_trace)

  return base.GradientTransformation(init_fn, update_fn)


def trace(x, /, *, offset=0, dtype=None):
    """
    Returns the sum along the specified diagonals of a matrix
    (or a stack of matrices) ``x``.

    This function is Array API compatible, contrary to
    :py:func:`numpy.trace`.

    Parameters
    ----------
    x : (...,M,N) array_like
        Input array having shape (..., M, N) and whose innermost two
        dimensions form MxN matrices.
    offset : int, optional
        Offset specifying the off-diagonal relative to the main diagonal,
        where::

            * offset = 0: the main diagonal.
            * offset > 0: off-diagonal above the main diagonal.
            * offset < 0: off-diagonal below the main diagonal.

    dtype : dtype, optional
        Data type of the returned array.

    Returns
    -------
    out : ndarray
        An array containing the traces and whose shape is determined by
        removing the last two dimensions and storing the traces in the last
        array dimension. For example, if x has rank k and shape:
        (I, J, K, ..., L, M, N), then an output array has rank k-2 and shape:
        (I, J, K, ..., L) where::

            out[i, j, k, ..., l] = trace(a[i, j, k, ..., l, :, :])

        The returned array must have a data type as described by the dtype
        parameter above.

    See Also
    --------
    numpy.trace

    Examples
    --------
    >>> np.linalg.trace(np.eye(3))
    3.0
    >>> a = np.arange(8).reshape((2, 2, 2))
    >>> np.linalg.trace(a)
    array([3, 11])

    Trace is computed with the last two axes as the 2-d sub-arrays.
    This behavior differs from :py:func:`numpy.trace` which uses the first two
    axes by default.

    >>> a = np.arange(24).reshape((3, 2, 2, 2))
    >>> np.linalg.trace(a).shape
    (3, 2)

    Traces adjacent to the main diagonal can be obtained by using the
    `offset` argument:

    >>> a = np.arange(9).reshape((3, 3)); a
    array([[0, 1, 2],
           [3, 4, 5],
           [6, 7, 8]])
    >>> np.linalg.trace(a, offset=1)  # First superdiagonal
    6
    >>> np.linalg.trace(a, offset=2)  # Second superdiagonal
    2
    >>> np.linalg.trace(a, offset=-1)  # First subdiagonal
    10
    >>> np.linalg.trace(a, offset=-2)  # Second subdiagonal
    6

    """
    return _core_trace(x, offset, axis1=-2, axis2=-1, dtype=dtype)


def trace(a, offset=0, axis1=0, axis2=1, dtype=None, out=None):
    """
    Return the sum along diagonals of the array.

    If `a` is 2-D, the sum along its diagonal with the given offset
    is returned, i.e., the sum of elements ``a[i,i+offset]`` for all i.

    If `a` has more than two dimensions, then the axes specified by axis1 and
    axis2 are used to determine the 2-D sub-arrays whose traces are returned.
    The shape of the resulting array is the same as that of `a` with `axis1`
    and `axis2` removed.

    Parameters
    ----------
    a : array_like
        Input array, from which the diagonals are taken.
    offset : int, optional
        Offset of the diagonal from the main diagonal. Can be both positive
        and negative. Defaults to 0.
    axis1, axis2 : int, optional
        Axes to be used as the first and second axis of the 2-D sub-arrays
        from which the diagonals should be taken. Defaults are the first two
        axes of `a`.
    dtype : dtype, optional
        Determines the data-type of the returned array and of the accumulator
        where the elements are summed. If dtype has the value None and `a` is
        of integer type of precision less than the default integer
        precision, then the default integer precision is used. Otherwise,
        the precision is the same as that of `a`.
    out : ndarray, optional
        Array into which the output is placed. Its type is preserved and
        it must be of the right shape to hold the output.

    Returns
    -------
    sum_along_diagonals : ndarray
        If `a` is 2-D, the sum along the diagonal is returned.  If `a` has
        larger dimensions, then an array of sums along diagonals is returned.

    See Also
    --------
    diag, diagonal, diagflat

    Examples
    --------
    >>> import numpy as np
    >>> np.trace(np.eye(3))
    3.0
    >>> a = np.arange(8).reshape((2,2,2))
    >>> np.trace(a)
    array([6, 8])

    >>> a = np.arange(24).reshape((2,2,2,3))
    >>> np.trace(a).shape
    (2, 3)

    """
    if isinstance(a, np.matrix):
        # Get trace of matrix via an array to preserve backward compatibility.
        return asarray(a).trace(
            offset=offset, axis1=axis1, axis2=axis2, dtype=dtype, out=out
        )
    else:
        return asanyarray(a).trace(
            offset=offset, axis1=axis1, axis2=axis2, dtype=dtype, out=out
        )


def trace(results_: _Sequence[_ods_ir.Type], message: _Union[str, _ods_ir.StringAttr], level: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, TraceOp]:
  op = TraceOp(results_=results_, message=message, level=level, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def trace(operand: _ods_ir.Value[_ods_ir.RankedTensorType], tag: _Union[str, _ods_ir.StringAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> TraceOp:
  return TraceOp(operand=operand, tag=tag, loc=loc, ip=ip)


def trace(
    log_dir: os.PathLike | str,
    create_perfetto_link=False,
    create_perfetto_trace=False,
    profiler_options: ProfileOptions | None = None,
):
  """Context manager to take a profiler trace.

  The trace will capture CPU, GPU, and/or TPU activity, including Python
  functions and JAX on-device operations.

  The resulting trace can be viewed with TensorBoard. Note that TensorBoard
  doesn't need to be running when collecting the trace.

  Only one trace may be collected at a time. A RuntimeError will be raised if a
  trace is started while another trace is running.

  Args:
    log_dir: The directory to save the profiler trace to (usually the
      TensorBoard log directory).
    create_perfetto_link: A boolean which, if true, creates and prints link to
      the Perfetto trace viewer UI (https://ui.perfetto.dev). The program will
      block until the link is opened and Perfetto loads the trace.
    create_perfetto_trace: A boolean which, if true, additionally dumps a
      ``perfetto_trace.json.gz`` file that is compatible for upload with the
      Perfetto trace viewer UI (https://ui.perfetto.dev). The file will also be
      generated if ``create_perfetto_link`` is true. This could be useful if you
      want to generate a Perfetto-compatible trace without blocking the process.
    profiler_options: Profiler options to configure the profiler for collection.
  """
  start_trace(
      log_dir, create_perfetto_link, create_perfetto_trace, profiler_options
  )
  try:
    yield
  finally:
    stop_trace()


def trace(a: ArrayLike, offset: int | ArrayLike = 0, axis1: int = 0, axis2: int = 1,
          dtype: DTypeLike | None = None, out: None = None) -> Array:
  """Calculate sum of the diagonal of input along the given axes.

  JAX implementation of :func:`numpy.trace`.

  Args:
    a: input array. Must have ``a.ndim >= 2``.
    offset: optional, int, default=0. Diagonal offset from the main diagonal.
      Can be positive or negative.
    axis1: optional, default=0. The first axis along which to take the sum of
      diagonal. Must be a static integer value.
    axis2: optional, default=1. The second axis along which to take the sum of
      diagonal. Must be a static integer value.
    dtype: optional. The dtype of the output array. Should be provided as static
      argument in JIT compilation.
    out: Not used by JAX.

  Returns:
    An array of dimension x.ndim-2 containing the sum of the diagonal elements
    along axes (axis1, axis2)

  See also:
    - :func:`jax.numpy.diag`: Returns the specified diagonal or constructs a diagonal
      array
    - :func:`jax.numpy.diagonal`: Returns the specified diagonal of an array.
    - :func:`jax.numpy.diagflat`: Returns a 2-D array with the flattened input array
      laid out on the diagonal.

  Examples:
    >>> x = jnp.arange(1, 9).reshape(2, 2, 2)
    >>> x
    Array([[[1, 2],
            [3, 4]],
    <BLANKLINE>
           [[5, 6],
            [7, 8]]], dtype=int32)
    >>> jnp.trace(x)
    Array([ 8, 10], dtype=int32)
    >>> jnp.trace(x, offset=1)
    Array([3, 4], dtype=int32)
    >>> jnp.trace(x, axis1=1, axis2=2)
    Array([ 5, 13], dtype=int32)
    >>> jnp.trace(x, offset=1, axis1=1, axis2=2)
    Array([2, 6], dtype=int32)
  """
  a = util.ensure_arraylike("trace", a)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.trace is not supported.")

  if _canonicalize_axis(axis1, np.ndim(a)) == _canonicalize_axis(axis2, np.ndim(a)):
    raise ValueError(f"axis1 and axis2 can not be same. axis1={axis1} and axis2={axis2}")

  if dtype is not None:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "trace")

  a_shape = np.shape(a)
  a = moveaxis(a, (axis1, axis2), (-2, -1))

  # Mask out the diagonal and reduce.
  a = where(eye(a_shape[axis1], a_shape[axis2], k=offset, dtype=bool),
            a, array_creation.zeros_like(a))
  return reductions.sum(a, axis=(-2, -1), dtype=dtype)


def trace(x: ArrayLike, /, *,
          offset: int = 0, dtype: DTypeLike | None = None) -> Array:
  """Compute the trace of a matrix.

  JAX implementation of :func:`numpy.linalg.trace`.

  Args:
    x: array of shape ``(..., M, N)`` and whose innermost two
      dimensions form MxN matrices for which to take the trace.
    offset: positive or negative offset from the main diagonal
      (default: 0).
    dtype: data type of the returned array (default: ``None``). If ``None``,
      then output dtype will match the dtype of ``x``, promoted to default
      precision in the case of integer types.

  Returns:
    array of batched traces with shape ``x.shape[:-2]``

  See also:
    - :func:`jax.numpy.trace`: similar API in the ``jax.numpy`` namespace.

  Examples:
    Trace of a single matrix:

    >>> x = jnp.array([[1,  2,  3,  4],
    ...                [5,  6,  7,  8],
    ...                [9, 10, 11, 12]])
    >>> jnp.linalg.trace(x)
    Array(18, dtype=int32)
    >>> jnp.linalg.trace(x, offset=1)
    Array(21, dtype=int32)
    >>> jnp.linalg.trace(x, offset=-1, dtype="float32")
    Array(15., dtype=float32)

    Batched traces:

    >>> x = jnp.arange(24).reshape(2, 3, 4)
    >>> jnp.linalg.trace(x)
    Array([15, 51], dtype=int32)
  """
  x = ensure_arraylike('jnp.linalg.trace', x)
  return jnp.trace(x, offset=offset, axis1=-2, axis2=-1, dtype=dtype)

