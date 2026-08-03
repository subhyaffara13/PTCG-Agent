from typing import Any, Callable

def smap(f: F, /, *,
         in_axes: int | None | InferFromArgs | tuple[Any, ...] = ...,
         out_axes: Any, axis_name: AxisName) -> F:
  ...


def smap(f: None = None, /, *,
         in_axes: int | None | InferFromArgs | tuple[Any, ...] = ...,
         out_axes: Any, axis_name: AxisName
         ) -> Callable[[G], G]:
  ...


def smap(f: F | None = None, /, *,
         in_axes: int | None | InferFromArgs | tuple[Any, ...] = Infer,
         out_axes: Any, axis_name: AxisName
         ) -> F | Callable[[G], G]:
  """Single axis shard_map that maps a function `f` one axis at a time.

  Args:
    f: Callable to be mapped. Each application of ``f``, or "instance" of ``f``,
      takes as input a shard of the mapped-over arguments and produces a shard
      of the output.
    in_axes: (optional) An integer, None, or sequence of values specifying which
      input array axes to map over. If not specified, `smap` will try to infer
      the axes from the arguments only under `Explicit` mode.
      An integer or ``None`` indicates which array axis to map over for all
      arguments (with ``None`` indicating not to map any axis), and a tuple
      indicates which axis to map for each corresponding positional argument.
      Axis integers must be in the range ``[-ndim, ndim)`` for each array,
      where ``ndim`` is the number of dimensions (axes) of the corresponding
      input array.
    out_axes: An integer, None, or (nested) standard Python container
      (tuple/list/dict) thereof indicating where the mapped axis should appear
      in the output.
    axis_name: ``mesh`` axis name over which the function ``f`` is manual.

  Returns:
    A callable representing a mapped version of ``f``, which accepts positional
    arguments corresponding to those of ``f`` and produces output corresponding
    to that of ``f``.
  """
  kwargs = dict(in_axes=in_axes, out_axes=out_axes, axis_name=axis_name)
  if f is None:
    return lambda g: _smap(g, **kwargs)
  return _smap(f, **kwargs)

