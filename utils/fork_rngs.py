
def fork_rngs(module: Module):
  """Context manager to fork rngs in a module."""
  if module.scope is None:
    yield
    return

  current_rngs = module.scope.rngs.copy()
  module.scope.rngs = {
      name: LazyRng.create(module.make_rng(name)) for name in current_rngs
  }

  try:
    yield
  finally:
    module.scope.rngs = current_rngs


def fork_rngs(
    node: tp.Any,
    /,
    *,
    split: (
        tp.Mapping[filterlib.Filter, int | tuple[int, ...] | None] | int | None
    ) = None,
    graph: bool | None = None,
    graph_updates: bool | None = None,
) -> SplitBackups:
  ...


def fork_rngs(
    *,
    split: (
        tp.Mapping[filterlib.Filter, int | tuple[int, ...] | None] | int | None
    ) = None,
    graph: bool | None = None,
    graph_updates: bool | None = None,
) -> tp.Callable[[F], F]:
  ...


def fork_rngs(
    node: tp.Any = MISSING,
    /,
    *,
    split: (
        tp.Mapping[filterlib.Filter, int | tuple[int, ...] | None] | int | None
    ) = None,
    graph: bool | None = None,
    graph_updates: bool | None = None,
) -> SplitBackups | tp.Callable[[F], F]:
  """Forks the (nested) Rng states of the given node.

  Args:
    node: the base node containing the rng states to fork.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references. If ``False``, uses
      tree-mode which treats Modules as regular JAX pytrees, avoiding
      the overhead of the graph protocol.

  Returns:
    A SplitBackups iterable if ``node`` is provided, otherwise a
    decorator that forks the rng states of the inputs to the
    decorated function.

  Example::

    >>> from flax import nnx
    ...
    >>> rngs = nnx.Rngs(params=0, dropout=1)
    >>> _ = nnx.fork_rngs(rngs)

  ``fork_rngs`` returns a SplitBackups object that can be used to restore the
  original unforked rng states using :func:`nnx.restore_rngs`, this is useful
  when you only want to fork the rng states temporarily::

    >>> rngs = nnx.Rngs(params=0, dropout=1)
    ...
    >>> backups = nnx.fork_rngs(rngs)
    >>> model = nnx.Linear(2, 3, rngs=rngs)
    >>> nnx.restore_rngs(backups)
    ...

  SplitBackups can also be used as a context manager to automatically restore
  the rng states when exiting the context::

    >>> rngs = nnx.Rngs(params=0, dropout=1)
    ...
    >>> with nnx.fork_rngs(rngs):
    ...   model = nnx.Linear(2, 3, rngs=rngs)

  """
  if graph is None:
    graph = graphlib.set_graph_mode.current_value()
  if graph_updates is None:
    graph_updates = graphlib.set_graph_updates.current_value()

  if isinstance(node, Missing):

    def fork_rngs_decorator(f: F) -> F:
      @functools.wraps(f)
      def fork_rngs_wrapper(*args, **kwargs):
        if graph and graph_updates:
          with fork_rngs(
              (args, kwargs), split=split, graph=True, graph_updates=True
          ):
            return f(*args, **kwargs)
        else:
          args, kwargs = fork_rngs(
              (args, kwargs), split=split, graph=graph, graph_updates=False
          )
          return f(*args, **kwargs)

      return tp.cast(F, fork_rngs_wrapper)

    return fork_rngs_decorator  # type: ignore[bad-return-type]

  if split is None:
    split = {...: None}
  elif isinstance(split, int | tuple):
    split = {...: split}

  predicate_splits = {
    filterlib.to_predicate(k): v for k, v in split.items()
  }

  if graph and graph_updates:
    return _graph_updates_fork_rngs(
        node, predicate_splits=predicate_splits, graph=graph
    )
  else:
    return _simple_fork_rngs(
        node, predicate_splits=predicate_splits, graph=graph
    )

