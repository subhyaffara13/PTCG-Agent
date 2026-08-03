import os
from typing import Any
from pathlib import Path


def unpack(stream, **kwargs):
    """
    Unpack an object from `stream`.

    Raises `ExtraData` when `stream` contains extra bytes.
    See :class:`Unpacker` for options.
    """
    data = stream.read()
    return unpackb(data, **kwargs)


def unpack(src_dir, dst_dir) -> None:
    """Move everything under `src_dir` to `dst_dir`, and delete the former."""
    for dirpath, dirnames, filenames in os.walk(src_dir):
        subdir = os.path.relpath(dirpath, src_dir)
        for f in filenames:
            src = os.path.join(dirpath, f)
            dst = os.path.join(dst_dir, subdir, f)
            os.renames(src, dst)
        for n, d in reversed(list(enumerate(dirnames))):
            src = os.path.join(dirpath, d)
            dst = os.path.join(dst_dir, subdir, d)
            if not os.path.exists(dst):
                # Directory does not exist in destination,
                # rename it and prune it from os.walk list.
                os.renames(src, dst)
                del dirnames[n]
    # Cleanup.
    for dirpath, dirnames, filenames in os.walk(src_dir, topdown=True):
        assert not filenames
        os.rmdir(dirpath)


def unpack(format: bytes | str, buffer: Buffer, /) -> tuple[Any, ...]:
    return struct.unpack(format, buffer)


def unpack(expr):
    """ Rule to unpack singleton args

    >>> from sympy.strategies import unpack
    >>> from sympy import Basic, S
    >>> unpack(Basic(S(2)))
    2
    """
    if len(expr.args) == 1:
        return expr.args[0]
    else:
        return expr


def unpack(x):
    if isinstance(x, Compound) and len(x.args) == 1:
        return x.args[0]
    else:
        return x


def unpack(path: str, dest: str = ".") -> None:
    """Unpack a wheel.

    Wheel content will be unpacked to {dest}/{name}-{ver}, where {name}
    is the package name and {ver} its version.

    :param path: The path to the wheel.
    :param dest: Destination directory (default to current directory).
    """
    with WheelFile(path) as wf:
        namever = wf.parsed_filename.group("namever")
        destination = Path(dest) / namever
        print(f"Unpacking to: {destination}...", end="", flush=True)
        for zinfo in wf.filelist:
            target_path = Path(wf.extract(zinfo, destination))

            # Set permissions to the same values as they were set in the archive
            # We have to do this manually due to
            # https://github.com/python/cpython/issues/59999
            permissions = zinfo.external_attr >> 16 & 0o777
            target_path.chmod(permissions)

    print("OK")


def unpack(stream, **kwargs):
    """
    Unpack an object from `stream`.

    Raises `ExtraData` when `stream` contains extra bytes.
    See :class:`Unpacker` for options.
    """
    data = stream.read()
    return unpackb(data, **kwargs)


def unpack(x):
  return tuple(unpack_dtype_p.bind(x))


def unpack(
    ab: jax.Array,
    /,
    *,
    format: PackFormat,
    preferred_element_type: jax.typing.DTypeLike | None = None,
) -> tuple[jax.Array, jax.Array]:
  """Unpacks two arrays according to the given format.

  .. warning:: This API is temporary and will be removed once the SparseCore
               compiler is able to do packing/unpacking automatically.

  Args:
    ab: The array to unpack.
    format: The packing format to use.
    preferred_element_type: Optional. The preferred element type of the unpacked
      arrays. If specified, must have double the bitwidth of the input array
      type.

  Returns:
    The unpacked arrays.
  """
  if preferred_element_type is not None:
    preferred_element_type = jnp.dtype(preferred_element_type)
  return unpack_p.bind(
      ab,
      format=format,
      preferred_element_type=preferred_element_type,
  )


def unpack(any_msg: Any, msg: Message) -> bool:
  return any_msg.Unpack(msg=msg)


def unpack(fmt, data, obj=None):
    if obj is None:
        obj = {}
    data = tobytes(data)
    formatstring, names, fixes = getformat(fmt)
    if isinstance(obj, dict):
        d = obj
    else:
        d = obj.__dict__
    elements = struct.unpack(formatstring, data)
    for i, name in enumerate(names.keys()):
        value = elements[i]
        if name in fixes:
            # fixed point conversion
            value = fi2fl(value, fixes[name])
        elif isinstance(value, bytes):
            try:
                value = tostr(value)
            except UnicodeDecodeError:
                pass
        d[name] = value
    return obj


def unpack(node: A, /, *, graph: bool | None = None) -> GraphState[A]:
  ...


def unpack(
    node: A, filter: filterlib.Filter, /, *, graph: bool | None = None
) -> GraphState[A]:
  ...


def unpack(
    node: A,
    filter1: filterlib.Filter,
    filter2: filterlib.Filter,
    /,
    *filters: filterlib.Filter,
    graph: bool | None = None,
) -> tuple[GraphState[A], ...]: ...


def unpack(
    node: A, *filters: filterlib.Filter, graph: bool | None = None
) -> GraphState[A] | tuple[GraphState[A], ...]:
  """Unpacks the state of a graph node into one or more :class:`GraphState` objects.

  ``unpack`` is similar to :func:`split` but instead of returning the
  :class:`GraphDef` as a separate value, it bundles it together with each
  :class:`State` into a :class:`GraphState` state. This avoids the need to carry
  the ``GraphDef`` in a separate variable.

  Example usage::

    >>> from flax import nnx
    >>> import jax, jax.numpy as jnp
    ...
    >>> class Foo(nnx.Module):
    ...   def __init__(self, rngs):
    ...     self.batch_norm = nnx.BatchNorm(2, rngs=rngs)
    ...     self.linear = nnx.Linear(2, 3, rngs=rngs)
    ...
    >>> node = Foo(nnx.Rngs(0))
    ...
    >>> state = nnx.unpack(node)
    >>> new_node = nnx.merge(state)
    >>> assert isinstance(new_node, Foo)

    Filters can also be provided to unpack multiple states into separate
    :class:`GraphState` groups::

    >>> params, batch_stats = nnx.unpack(node, nnx.Param, nnx.BatchStat)
    >>> new_node = nnx.merge(params, batch_stats)
    >>> assert isinstance(new_node, Foo)

  :class:`GraphState` instances can often be used as a drop-in replacement for
  :class:`State` objects.

  Args:
    node: A graph node to unpack.
    *filters: One or more filters to partition the state into mutually
      exclusive groups. If a single filter (or none) is provided, a single
      :class:`GraphState` is returned. If two or more filters are provided,
      a tuple of :class:`GraphState` objects is returned.
    graph: If ``True``, uses graph-mode which supports the full
      NNX feature set including shared references. If ``False``, uses
      tree-mode which treats Modules as regular JAX pytrees, avoiding
      the overhead of the graph protocol.
  Returns:
    A single :class:`GraphState` if zero or one filter is passed, or a tuple
    of :class:`GraphState` objects if two or more filters are passed.
  """
  graphdef, *states = split(node, *filters, graph=graph)
  if len(states) == 1:
    return GraphState(graphdef, states[0])  # type: ignore[bad-return-type]
  return tuple(GraphState(graphdef, state) for state in states)  # type: ignore[bad-return-type]

