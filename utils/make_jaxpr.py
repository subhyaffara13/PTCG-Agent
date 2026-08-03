import functools
from typing import Any, Callable

def make_jaxpr(
    fun: Callable,
    static_argnums: int | Sequence[int] = (),
    axis_env: Sequence[tuple[AxisName, int]] | None = None,
    return_shape: Literal[False] = ...,
) -> Callable[..., core.ClosedJaxpr]:
  ...


def make_jaxpr(
    fun: Callable,
    static_argnums: int | Sequence[int] = (),
    axis_env: Sequence[tuple[AxisName, int]] | None = None,
    return_shape: Literal[True] = ...,
) -> Callable[..., tuple[core.ClosedJaxpr, Any]]:
  ...


def make_jaxpr(
    fun: Callable,
    static_argnums: int | Sequence[int] = (),
    axis_env: Sequence[tuple[AxisName, int]] | None = None,
    return_shape: bool = False,
) -> Callable[..., core.ClosedJaxpr | tuple[core.ClosedJaxpr, Any]]:
  """Create a function that returns the jaxpr of ``fun`` given example args.

  Args:
    fun: The function whose ``jaxpr`` is to be computed. Its positional
      arguments and return value should be arrays, scalars, or standard Python
      containers (tuple/list/dict) thereof.
    static_argnums: See the :py:func:`jax.jit` docstring.
    axis_env: Optional, a sequence of pairs where the first element is an axis
      name and the second element is a positive integer representing the size of
      the mapped axis with that name. This parameter is useful when lowering
      functions that involve parallel communication collectives, and it
      specifies the axis name/size environment that would be set up by
      applications of :py:func:`jax.pmap`.
    return_shape: Optional boolean, defaults to ``False``. If ``True``, the
      wrapped function returns a pair where the first element is the
      ``ClosedJaxpr`` representation of ``fun`` and the second element is a
      pytree with the same structure as the output of ``fun`` and where the
      leaves are objects with ``shape`` and ``dtype`` attributes representing
      the corresponding types of the output leaves.

  Returns:
    A wrapped version of ``fun`` that when applied to example arguments returns
    a ``ClosedJaxpr`` representation of ``fun`` on those arguments. If the
    argument ``return_shape`` is ``True``, then the returned function instead
    returns a pair where the first element is the ``ClosedJaxpr``
    representation of ``fun`` and the second element is a pytree representing
    the structure, shape, dtypes, and named shapes of the output of ``fun``.

  A ``jaxpr`` is JAX's intermediate representation for program traces. The
  ``jaxpr`` language is based on the simply-typed first-order lambda calculus
  with let-bindings. :py:func:`make_jaxpr` adapts a function to return its
  ``jaxpr``, which we can inspect to understand what JAX is doing internally.
  The ``jaxpr`` returned is a trace of ``fun`` abstracted to
  :py:class:`ShapedArray` level. Other levels of abstraction exist internally.

  We do not describe the semantics of the ``jaxpr`` language in detail here, but
  instead give a few examples.

  >>> import jax
  >>>
  >>> def f(x): return jax.numpy.sin(jax.numpy.cos(x))
  >>> print(f(3.0))
  -0.83602
  >>> jax.make_jaxpr(f)(3.0)
  { lambda ; a:f32[]. let b:f32[] = cos a; c:f32[] = sin b in (c,) }
  >>> jax.make_jaxpr(jax.grad(f))(3.0)
  { lambda ; a:f32[]. let
      b:f32[] = cos a
      c:f32[] = sin a
      _:f32[] = sin b
      d:f32[] = cos b
      e:f32[] = mul 1.0:f32[] d
      f:f32[] = neg e
      g:f32[] = mul f c
    in (g,) }
  """
  try:
    hash(fun)
    weakref.ref(fun)
  except TypeError:
    fun = partial(fun)

  @wraps(fun)
  @api_boundary
  def make_jaxpr_f(*args, **kwargs):
    with core.extend_axis_env_nd(axis_env or []):
      traced = jit(fun, static_argnums=static_argnums).trace(*args, **kwargs)
    # `jit` converts tracers in consts to args but `make_jaxpr` callers expect
    # consts not to be converted.
    num_consts = traced._num_consts
    if num_consts:
      jaxpr_ = pe.convert_invars_to_constvars(traced.jaxpr.jaxpr, num_consts)
      jaxpr = core.ClosedJaxpr(jaxpr_, traced._consts)
    else:
      jaxpr = traced.jaxpr
    if return_shape:
      return jaxpr, traced.out_info
    return jaxpr

  make_jaxpr_f.__module__ = "jax"
  if hasattr(fun, "__qualname__"):
    make_jaxpr_f.__qualname__ = f"make_jaxpr({fun.__qualname__})"
  if hasattr(fun, "__name__"):
    make_jaxpr_f.__name__ = f"make_jaxpr({fun.__name__})"
  return make_jaxpr_f


def make_jaxpr(f, *args, **kwargs):
  flat_args, in_tree = tree_util.tree_flatten((args, kwargs))
  flat_avals = [core.shaped_abstractify(x) for x in flat_args]
  debug_info = api_util.debug_info('make_jaxpr', f, args, kwargs)
  flat_fun, out_tree_thunk = api_util.flatten_fun(
      lu.wrap_init(f, debug_info=debug_info), in_tree
  )
  jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(flat_fun, flat_avals)
  out_tree = out_tree_thunk()
  return jaxpr, consts, in_tree, out_tree


def make_jaxpr(
  f: tp.Callable[..., A],
  *,
  graph: bool | None = None,
  graph_updates: bool | None = None,
  static_argnums: int | tp.Sequence[int] = (),
) -> tp.Callable[..., tp.Any]: ...


def make_jaxpr(
  *,
  graph: bool | None = None,
  graph_updates: bool | None = None,
  static_argnums: int | tp.Sequence[int] = (),
) -> tp.Callable[[F], tp.Callable[..., tp.Any]]: ...


def make_jaxpr(
  f: tp.Callable[..., A] | Missing = MISSING,
  *,
  graph: bool | None = None,
  graph_updates: bool | None = None,
  static_argnums: int | tp.Sequence[int] = (),
) -> tp.Callable[..., tp.Any] | tp.Callable[[F], tp.Callable[..., tp.Any]]:
  """A "lifted" version of `jax.make_jaxpr <https://jax.readthedocs.io/en/latest/jaxpr.html>`_
    that can handle `flax.nnx.Module <https://flax.readthedocs.io/en/latest/api_reference/flax.nnx/module.html#flax.nnx.Module>`_
    / graph nodes as arguments.

  Args:
    f: the function to be transformed into a Jaxpr.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references and reference semantics.
      If ``False``, uses tree-mode which treats Modules as regular JAX
      pytrees, avoiding the overhead of the graph protocol.
    graph_updates: If ``True``, propagates updates on graph structure
      that happen inside the transform to the input graphs, has no
      effect when ``graph=False``. ``nnx.make_jaxpr`` raises an error
      if ``graph_updates=True``.
    static_argnums: Optional, int or sequence of ints. Specifies which
      positional argument(s) to treat as static (compile-time constant).
  """
  if isinstance(f, Missing):
    return functools.partial(
      make_jaxpr,
      graph=graph,
      graph_updates=graph_updates,
      static_argnums=static_argnums,
    )

  if graph_updates is None:
    graph_updates = graphlib.set_graph_updates.current_value()
  if graph_updates:
    raise ValueError('nnx.make_jaxpr does not support graph_updates=True.')

  f_call, _, was_bound = _resolve_bound_callable(f)
  if was_bound:
    _raise_bound_method_error('make_jaxpr')
  if graph is None:
    graph = graphlib.set_graph_mode.current_value()

  jaxpr_maker = jax.make_jaxpr(
    SimpleMakeJaxprFn(f_call, graph=graph),
    static_argnums=static_argnums,
  )

  @functools.wraps(f)
  def jaxpr_wrapper(*args, **kwargs):
    if graph:
      args, kwargs = extract.to_tree2((args, kwargs))
    extract.check_no_aliases('make_jaxpr', args=args, kwargs=kwargs)
    jaxpr = jaxpr_maker(*args, **kwargs)
    return jaxpr

  return jaxpr_wrapper

