
def with_rngs(
    node: A,
    /,
    *,
    split: (
        tp.Mapping[filterlib.Filter, int | tuple[int, ...]]
        | int
        | tuple[int, ...]
        | None
    ) = None,
    fork: filterlib.Filter | tp.Sequence[filterlib.Filter] | None = None,
    broadcast: (
        tp.Mapping[filterlib.Filter, int | tuple[int, ...]]
        | int
        | tuple[int, ...]
        | None
    ) = None,
    only: filterlib.Filter = True,
    graph: bool | None = None,
    graph_updates: bool | None = None,
) -> A: ...


def with_rngs(
    *,
    split: (
        tp.Mapping[filterlib.Filter, int | tuple[int, ...]]
        | int
        | tuple[int, ...]
        | None
    ) = None,
    fork: filterlib.Filter | tp.Sequence[filterlib.Filter] | None = None,
    broadcast: (
        tp.Mapping[filterlib.Filter, int | tuple[int, ...]]
        | int
        | tuple[int, ...]
        | None
    ) = None,
    only: filterlib.Filter = True,
    graph: bool | None = None,
    graph_updates: bool | None = None,
) -> tp.Callable[[F], F]: ...


def with_rngs(
    node: tp.Any = MISSING,
    /,
    *,
    split: (
        tp.Mapping[filterlib.Filter, int | tuple[int, ...]]
        | int
        | tuple[int, ...]
        | None
    ) = None,
    fork: filterlib.Filter | tp.Sequence[filterlib.Filter] | None = None,
    broadcast: (
        tp.Mapping[filterlib.Filter, int | tuple[int, ...]]
        | int
        | tuple[int, ...]
        | None
    ) = None,
    only: filterlib.Filter = True,
    graph: bool | None = None,
    graph_updates: bool | None = None,
) -> tp.Any:
  """Returns a copy of ``tree`` with ``RngStream`` objects replaced according to

  ``split`` and ``fork`` rules.

  ``split`` controls which streams are **split** — after splitting, each call
  to the stream produces one key from an array of pre-generated keys rather
  than a single key.  ``fork`` controls which of the remaining streams are
  **forked** — each call to a forked stream produces a unique key derived from
  the parent counter.  Streams that match neither rule are returned unchanged.

  Args:
    node: A pytree that may contain ``RngStream`` objects (e.g. an ``Rngs``
      instance, a module, or any nested structure).
    split: Specifies which streams to split and into what shape.  Can be:  * An
      ``int`` or ``tuple[int, ...]`` — split *all* streams into this shape,
      equivalent to ``{...: split}``. * A
      :class:`~flax.nnx.filterlib.Filter`-keyed mapping where each value is an
      ``int`` or ``tuple[int, ...]``.  The first matching filter wins.
    fork: A :class:`~flax.nnx.filterlib.Filter`, a sequence of filters, or
      ``None`` selecting which streams not already handled by ``split`` should
      be forked.  Pass ``...`` to fork all remaining streams.
    broadcast: Specifies which streams to broadcast and into what shape.  Can
      be: * An ``int`` or ``tuple[int, ...]`` — broadcast *all* streams into
        this shape, equivalent to ``{...: broadcast}``. * A
        :class:`~flax.nnx.filterlib.Filter`-keyed mapping where each value is an
        ``int`` or ``tuple[int, ...]``.  The first matching filter wins.
    only: A :class:`~flax.nnx.filterlib.Filter` selecting which streams to
      process. Pass ``True`` (default) to process all streams.
    graph: If ``True``, uses graph-mode which supports the full NNX feature set
      including shared references. If ``False``, uses tree-mode which treats
      Modules as regular JAX pytrees, avoiding the overhead of the graph
      protocol.

  Returns:
    A new tree of the same structure as ``tree`` with ``RngStream`` objects
    replaced by split or forked copies as specified.

  Example — split all streams::

    >>> from flax import nnx
    ...
    >>> rngs = nnx.Rngs(params=0, dropout=1)
    >>> new_rngs = nnx.with_rngs(rngs, split=4, graph=False)
    >>> new_rngs.params.key.shape
    (4,)
    >>> new_rngs.dropout.key.shape
    (4,)

  Example — split some streams, fork the rest::

    >>> rngs = nnx.Rngs(params=0, dropout=1)
    >>> new_rngs = nnx.with_rngs(
    ...   rngs, split={'params': 4}, fork=nnx.Not('params'), graph=False
    ... )
    >>> new_rngs.params.key.shape
    (4,)
    >>> new_rngs.dropout.key.shape   # forked: scalar key, advanced counter
    ()

  Example — per-filter split shapes::

    >>> rngs = nnx.Rngs(params=0, dropout=1, noise=2)
    >>> new_rngs = nnx.with_rngs(rngs, split={
    ...   'params': 4,    # split params into 4 keys
    ...   ...: (2, 4),    # split anything else into 2×4 keys
    ... }, graph=False)
    >>> new_rngs.params.key.shape
    (4,)
    >>> new_rngs.noise.key.shape
    (2, 4)
  """
  if graph is None:
    graph = graphlib.set_graph_mode.current_value()
  if graph_updates is None:
    graph_updates = graphlib.set_graph_updates.current_value()

  if graph and graph_updates:
    raise NotImplementedError(
        'graph=True and graph_updates=True is not supported for `with_rngs`'
    )

  if isinstance(node, Missing):

    def with_rngs_decorator(f: F) -> F:
      @functools.wraps(f)
      def with_rngs_wrapper(*args, **kwargs):
        args, kwargs = with_rngs(
            (args, kwargs),
            split=split,
            fork=fork,
            broadcast=broadcast,
            only=only,
            graph=graph,
            graph_updates=False,
        )
        return f(*args, **kwargs)

      return tp.cast(F, with_rngs_wrapper)

    return with_rngs_decorator  # type: ignore[bad-return-type]

  if split is None:
    split = {}
  elif isinstance(split, (int, tuple)):
    split = {...: split}

  if broadcast is None:
    broadcast = {}
  elif isinstance(broadcast, (int, tuple)):
    broadcast = {...: broadcast}

  if fork is None:
    fork = []
  elif isinstance(fork, str) or not isinstance(fork, tp.Sequence):
    fork = [fork]

  split_predicates = [(k, filterlib.to_predicate(k), v) for k, v in split.items()]
  broadcast_predicates = [(k, filterlib.to_predicate(k), v) for k, v in broadcast.items()]
  fork_predicates = [(p, filterlib.to_predicate(p)) for p in fork]
  only_predicate = filterlib.to_predicate(only)

  def update_rngs(path, val):
    if isinstance(val, RngStream) and only_predicate(path, val):
      results = {}
      for (filter, predicate, num_splits) in split_predicates:
        if predicate(path, val):
          results['split'] = (filter, num_splits)
          break
      for (filter, predicate, num_broadcasts) in broadcast_predicates:
        if predicate(path, val):
          results['broadcast'] = (filter, num_broadcasts)
          break
      for (filter, predicate) in fork_predicates:
        if predicate(path, val):
          results['fork'] = (filter,)
          break

      if len(results) > 1:
        specific_matches = [r for r, info in results.items() if info[0] not in (..., True)]
        if len(specific_matches) > 1:
          rule_descriptions = '\n'.join(f'  - {rule} matches filter {info[0]!r}' for rule, info in results.items())
          raise ValueError(
            f"RngStream at path {path} matches multiple rules:\n{rule_descriptions}"
          )

      if 'split' in results:
        return val.split(results['split'][1])
      if 'broadcast' in results:
        return val.broadcast(results['broadcast'][1])
      if 'fork' in results:
        return val.fork()
    return val

  return graphlib.recursive_map(update_rngs, node, graph=graph)

