import functools
import logging
from typing import Any, Callable

def debug_print(format: _Union[str, _ods_ir.StringAttr], value: _ods_ir.Value[_ods_ir.VectorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> DebugPrintOp:
  return DebugPrintOp(format=format, value=value, loc=loc, ip=ip)


def debug_print(
    fmt: str,
    *args: Any,
    ordered: bool = False,
    partitioned: bool = False,
    skip_format_check: bool = False,
    _use_logging: bool = False,
    **kwargs: Any,
) -> None:
  ...


def debug_print(
    *,
    ordered: bool = False,
    partitioned: bool = False,
    skip_format_check: bool = False,
    _use_logging: bool = False,
) -> Callable[..., None]:
  ...


def debug_print(
    fmt: str | None = None,
    *args,
    ordered: bool = False,
    partitioned: bool = False,
    skip_format_check: bool = False,
    _use_logging: bool = False,
    **kwargs,
) -> Callable[..., None] | None:
  """Prints values and works in staged out JAX functions.

  This function does *not* work with f-strings because formatting is delayed.
  So instead of ``jax.debug.print(f"hello {bar}")``, write
  ``jax.debug.print("hello {bar}", bar=bar)``.

  ``jax.debug.print`` supports two ways of being called:

  1. Two-call form (Recommended):
     ``jax.debug.print(ordered=True)("hello {x}", x=42)``
     Options are passed in the first call. The format string and arguments are
     passed in the second call. No option arguments are accepted in the second
     call.

  2. Single-call form:
     ``jax.debug.print("hello {x}", x=42, ordered=True)``
     (Soft deprecated) Mixing `ordered` and `partitioned` options with print
     ``kwargs`` is soft deprecated.

  Args:
    fmt: A format string, e.g. ``"hello {x}"``, that will be used to format
      input arguments, like ``str.format``. See the Python docs on `string
      formatting <https://docs.python.org/3/library/stdtypes.html#str.format>`_
      and `format string syntax
      <https://docs.python.org/3/library/string.html#formatstrings>`_.
    *args: A list of positional arguments to be formatted, as if passed to
      ``fmt.format``.
    ordered: A keyword only argument used to indicate whether or not the staged
      out computation will enforce ordering of this ``jax.debug.print`` w.r.t.
      other ordered ``jax.debug.print`` calls.
    partitioned: If True, then print local shards only; this option avoids an
      all-gather of the operands. If False, print with logical operands; this
      option requires an all-gather of operands first.
    skip_format_check: If True, the format string is not checked. This is useful
      when using the function from inside a Pallas TPU kernel, where scalars
      args will be printed after the format string.
    **kwargs: Additional keyword arguments to be formatted, as if passed to
      ``fmt.format``.
  """
  def _debug_print(fmt: str, *c_args, **c_kwargs):
    if not skip_format_check:
      # Check that we provide the correct arguments to be formatted.
      formatter.format(fmt, *c_args, **c_kwargs)
    has_placeholders = False
    if fmt:
      _, field_name, *_ = next(iter(string.Formatter().parse(fmt)))
      has_placeholders = field_name is not None
    in_tree, dyn_args, static_args = _split_callback_args(c_args, c_kwargs)
    static_args = tuple(static_args.items())
    np_printoptions = tuple(np.get_printoptions().items())

    debug_print_p.bind(
        *dyn_args,
        fmt=fmt,
        ordered=ordered,
        partitioned=partitioned,
        in_tree=in_tree,
        static_args=static_args,
        np_printoptions=np_printoptions,
        has_placeholders=has_placeholders,
        logging_record=(
            _make_logging_record(logging.INFO) if _use_logging else None
        ),
    )

  if fmt is not None:
    _debug_print(fmt, *args, **kwargs)
    return None
  if args or kwargs:
    raise TypeError(
        "debug_print received unexpected arguments in the two-call form:"
        f" {args=} {kwargs=}"
    )
  return _debug_print


def debug_print(fmt: str, *args: jax_typing.ArrayLike):
  """Prints values from inside a Pallas kernel.

  Args:
    fmt: A format string to be included in the output. The restrictions on the
      format string depend on the backend:

      * On GPU, when using Triton, ``fmt`` must not contain any placeholders
        (``{...}``), since it is always printed before any of the values.
      * On GPU, when using the experimental Mosaic GPU backend, ``fmt`` must
        contain a placeholder for each value to be printed. Format specs and
        conversions are not supported. If a single value is provided, the value
        may be an array. Otherwise, all values must be scalars.
      * On TPU, if all inputs are scalars: If ``fmt`` contains placeholders,
        all values must be 32-bit integers. If there are no placeholders, the
        values are printed after the format string.
      * On TPU, if the input is a single vector, the vector is printed after
        the format string. The format string must end with a single placeholder
        ``{}``.
    *args: The values to print.
  """
  return debugging.debug_print(fmt, *args, skip_format_check=True)


def debug_print(fmt, *args, uniform=True, scope=None):
  if not uniform and scope is not None:
    raise ValueError("Cannot specify scope to a non-uniform debug_print.")
  if scope is None:
    scope = ThreadSubset.WARPGROUP
  type_formats = []
  new_args = []
  for arg in args:
    if isinstance(arg.type, ir.VectorType):
      vec_ty = ir.VectorType(arg.type)
      if len(vec_ty.shape) > 1:
        raise NotImplementedError(
            f"2D+ vectors are not supported in debug_print: {vec_ty}"
        )
      vec_args = [
          vector.extract(
              arg,
              dynamic_position=[],
              static_position=ir.DenseI64ArrayAttr.get([i]),
          )
          for i in range(vec_ty.shape[0])
      ]
      ty_formats, args = zip(*map(_debug_scalar_ty_format, vec_args))
      ty_format = f"[{','.join(ty_formats)}]"
      new_args += args
    else:
      ty_format, arg = _debug_scalar_ty_format(arg)
      new_args.append(arg)

    if ty_format is None:
      raise NotImplementedError(arg.type)
    type_formats.append(ty_format)
  ctx = (
      functools.partial(single_thread, scope=scope)
      if uniform
      else contextlib.nullcontext
  )
  with ctx():
    gpu.printf(fmt.format(*type_formats) + "\n", *new_args)

