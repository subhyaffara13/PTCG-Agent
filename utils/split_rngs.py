import functools

def split_rngs(
    node: tp.Any,
    /,
    *,
    splits: int | tuple[int, ...],
    only: filterlib.Filter = ...,
    squeeze: bool = False,
    graph: tp.Literal[True] | None = None,
    graph_updates: tp.Literal[True] | None = None,
) -> SplitBackups:
  ...


def split_rngs(
    node: A,
    /,
    *,
    splits: int | tuple[int, ...],
    only: filterlib.Filter = ...,
    squeeze: bool = False,
    graph: tp.Literal[False],
    graph_updates: bool | None = None,
) -> A:
  ...


def split_rngs(
    node: A,
    /,
    *,
    splits: int | tuple[int, ...],
    only: filterlib.Filter = ...,
    squeeze: bool = False,
    graph: tp.Literal[True] | None,
    graph_updates: tp.Literal[False],
) -> A:
  ...


def split_rngs(
    *,
    splits: int | tuple[int, ...],
    only: filterlib.Filter = ...,
    squeeze: bool = False,
    graph: bool | None = None,
    graph_updates: bool | None = None,
) -> tp.Callable[[F], F]:
  ...


def split_rngs(
    node: tp.Any = MISSING,
    /,
    *,
    splits: int | tuple[int, ...],
    only: filterlib.Filter = ...,
    squeeze: bool = False,
    graph: bool | None = None,
    graph_updates: bool | None = None,
) -> SplitBackups | tp.Any | tp.Callable[[F], F]:
  """Splits the (nested) Rng states of the given node.

  Args:
    node: the base node containing the rng states to split.
    splits: an integer or tuple of integers specifying the shape of the split
      rng keys.
    only: a Filter selecting which rng states to split.
    graph: If ``True`` (default), uses graph-mode which supports the full NNX
      feature set including shared references. If ``False``, uses tree-mode
      which treats Modules as regular JAX pytrees, avoiding the overhead of the
      graph protocol.
    graph_updates: If ``True``, applies the splits in-place on the node. If
      ``False``, returns a new node with split rng states.

  Returns:
    A SplitBackups iterable if ``node`` is provided, otherwise a
    decorator that splits the rng states of the inputs to the
    decorated function.

  Example::

    >>> from flax import nnx
    ...
    >>> rngs = nnx.Rngs(params=0, dropout=1)
    >>> _ = nnx.split_rngs(rngs, splits=5)
    >>> rngs.params.key.shape, rngs.dropout.key.shape
    ((5,), (5,))

    >>> rngs = nnx.Rngs(params=0, dropout=1)
    >>> _ = nnx.split_rngs(rngs, splits=(2, 5))
    >>> rngs.params.key.shape, rngs.dropout.key.shape
    ((2, 5), (2, 5))


    >>> rngs = nnx.Rngs(params=0, dropout=1)
    >>> _ = nnx.split_rngs(rngs, splits=5, only='params')
    >>> rngs.params.key.shape, rngs.dropout.key.shape
    ((5,), ())

  Once split, random state can be used with transforms like :func:`nnx.vmap`::

    >>> class Model(nnx.Module):
    ...   def __init__(self, rngs):
    ...     self.linear = nnx.Linear(2, 3, rngs=rngs)
    ...     self.dropout = nnx.Dropout(0.5, rngs=rngs)
    ...
    >>> rngs = nnx.Rngs(params=0, dropout=1)
    >>> _ = nnx.split_rngs(rngs, splits=5, only='params')
    ...
    >>> state_axes = nnx.StateAxes({(nnx.Param, 'params'): 0, ...: None})
    ...
    >>> @nnx.vmap(in_axes=(state_axes,), out_axes=state_axes)
    ... def create_model(rngs):
    ...   return Model(rngs)
    ...
    >>> model = create_model(rngs)
    >>> model.dropout.rngs.key.shape
    ()

  ``split_rngs`` returns a SplitBackups object that can be used to restore the
  original unsplit rng states using :func:`nnx.restore_rngs`, this is useful
  when you only want to split the rng states temporarily::

    >>> rngs = nnx.Rngs(params=0, dropout=1)
    ...
    >>> backups = nnx.split_rngs(rngs, splits=5, only='params')
    >>> model = create_model(rngs)
    >>> nnx.restore_rngs(backups)
    ...
    >>> model.dropout.rngs.key.shape
    ()

  SplitBackups can also be used as a context manager to automatically restore
  the rng states when exiting the context::

    >>> rngs = nnx.Rngs(params=0, dropout=1)
    ...
    >>> with nnx.split_rngs(rngs, splits=5, only='params'):
    ...   model = create_model(rngs)
    ...
    >>> model.dropout.rngs.key.shape
    ()

    >>> state_axes = nnx.StateAxes({(nnx.Param, 'params'): 0, ...: None})
    ...
    >>> @nnx.split_rngs(splits=5, only='params')
    ... @nnx.vmap(in_axes=(state_axes,), out_axes=state_axes)
    ... def create_model(rngs):
    ...   return Model(rngs)
    ...
    >>> rngs = nnx.Rngs(params=0, dropout=1)
    >>> model = create_model(rngs)
    >>> model.dropout.rngs.key.shape
    ()
  """
  if graph is None:
    graph = graphlib.set_graph_mode.current_value()
  if graph_updates is None:
    graph_updates = graphlib.set_graph_updates.current_value()

  if isinstance(node, Missing):

    def split_rngs_decorator(f: F) -> F:
      @functools.wraps(f)
      def split_rngs_wrapper(*args, **kwargs):
        if graph and graph_updates:
          with split_rngs(
              (args, kwargs),
              splits=splits,
              only=only,
              squeeze=squeeze,
              graph=True,
              graph_updates=True,
          ):
            return f(*args, **kwargs)
        else:
          args, kwargs = split_rngs(
              (args, kwargs),
              splits=splits,
              only=only,
              squeeze=squeeze,
              graph=graph,
              graph_updates=False,
          )
          return f(*args, **kwargs)

      return tp.cast(F, split_rngs_wrapper)

    return split_rngs_decorator  # type: ignore[bad-return-type]

  if squeeze and splits != 1:
    raise ValueError('squeeze=True is only supported for splits=1')

  if graph and graph_updates:
    return _graph_updates_split_rngs(
        node,
        splits=splits,
        only=only,
        squeeze=squeeze,
    )
  else:
    return _simple_split_rngs(
        node,
        splits=splits,
        only=only,
        squeeze=squeeze,
        graph=graph,
    )

