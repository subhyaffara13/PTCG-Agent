import functools
from typing import Callable

def remat(fun: Callable, *, prevent_cse: bool = True,
          policy: Callable[..., bool] | None = None,
          static_argnums: int | tuple[int, ...] = (),
          concrete: bool | DeprecatedArg = DeprecatedArg()) -> Callable:
  """Alias of :func:`jax.checkpoint`."""
  return checkpoint(fun, prevent_cse=prevent_cse, policy=policy,
                    static_argnums=static_argnums, concrete=concrete)


def remat(
    target,
    variables=True,
    rngs=True,
    concrete=False,
    prevent_cse=True,
    static_argnums=(),
    policy=None,
    methods=None,
):
  """Flax lifted remat that supports static_argnums."""
  return flax.linen.transforms.lift_transform(
      core_remat_static,
      target,
      variables=variables,
      rngs=rngs,
      concrete=concrete,
      prevent_cse=prevent_cse,
      static_argnums=static_argnums,
      policy=policy,
      methods=methods,
  )


def remat(
  *,
  prevent_cse: bool = True,
  static_argnums: int | tuple[int, ...] = (),
  policy: tp.Callable[..., bool] | None = None,
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> tp.Callable[[F], F]: ...


def remat(
  f: F,
  *,
  prevent_cse: bool = True,
  static_argnums: int | tuple[int, ...] = (),
  policy: tp.Callable[..., bool] | None = None,
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> F: ...


def remat(
  f: F | Missing = MISSING,
  *,
  prevent_cse: bool = True,
  static_argnums: int | tuple[int, ...] = (),
  policy: tp.Callable[..., bool] | None = None,
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> F | tp.Callable[[F], F]:
  """A 'lifted' version of the
  `jax.checkpoint <https://jax.readthedocs.io/en/latest/_autosummary/jax.checkpoint.html>`__
  (a.k.a. ``jax.remat``).

  ``flax.nnx.remat``, similar to ``jax.checkpoint`` can provide control over, for
    example, how ``flax.nnx.grad`` values are computed and saved during the forward pass versus
    how they are recomputed during the backward pass, trading off memory and FLOPs.

  Learn more in `Flax NNX vs JAX Transformations <https://flax.readthedocs.io/en/latest/guides/jax_and_nnx_transforms.html>`_.

  To learn about ``jax.remat``, go to JAX's
    `fundamentals of jax.checkpoint <https://jax.readthedocs.io/en/latest/notebooks/autodiff_remat.html#fundamentals-of-jax-checkpoint>`_
    and `practical notes <https://jax.readthedocs.io/en/latest/notebooks/autodiff_remat.html#practical-notes>`_.

  Args:
    f: Function to be rematerialized.
    prevent_cse: Optional, bool. If True, prevents common subexpression
      elimination. Default True.
    static_argnums: Optional, int or tuple of ints. Specifies which
      positional arguments to treat as static.
    policy: Optional, callable. A policy for which intermediates to save
      during the forward pass.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references and reference semantics.
      If ``False``, uses tree-mode which treats Modules as regular JAX
      pytrees, avoiding the overhead of the graph protocol. Tree-mode does
      not support shared ``Variable`` references.
    graph_updates: If ``True``, propagates updates on graph structure
      that happen inside the transform to the input graphs, has no
      effect when ``graph=False``.
  """
  if graph is None:
    graph = graphlib.set_graph_mode.current_value()
  if graph_updates is None:
    graph_updates = graphlib.set_graph_updates.current_value()
  if isinstance(f, Missing):
    return functools.partial(
      remat,
      prevent_cse=prevent_cse,
      static_argnums=static_argnums,
      policy=policy,
      graph=graph,
      graph_updates=graph_updates,
    )  # type: ignore[return-value]

  f_unbound, _, was_bound = _resolve_bound_callable(f)

  if was_bound:
    _raise_bound_method_error('remat')

  if not graph or not graph_updates:
    checkpointed_fn = jax.checkpoint(
      SimpleRematFn(f_unbound, graph=graph),
      prevent_cse=prevent_cse,
      static_argnums=static_argnums,
      policy=policy,
    )

    @functools.wraps(f_unbound)
    def simple_remat_wrapper(*args, **kwargs):
      if graph:
        args, kwargs = extract.to_tree2((args, kwargs))
      extract.check_no_aliases('remat', args=args, kwargs=kwargs)
      out, updates = checkpointed_fn(*args, **kwargs)
      if graph:
        out = extract.from_tree2(out)
      extract.apply_variable_updates((args, kwargs), updates)
      return out

    return simple_remat_wrapper  # type: ignore[return-value]

  # Unbound function path: preserve the concise composition used in NNX.
  return resolve_kwargs()(  # type: ignore[return-value]
    graphlib.update_context('remat')(
      general.split_inputs(
        jax.checkpoint(
          general.merge_inputs(f_unbound, ctxtag='remat'),
          prevent_cse=prevent_cse,
          static_argnums=static_argnums,
          policy=policy,
        ),
        ctxtag='remat',
      ),
    )
  )

