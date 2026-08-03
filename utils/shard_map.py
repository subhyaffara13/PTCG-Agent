import functools
from typing import Callable, Set

def shard_map(f, mesh, in_specs, out_specs, check_rep=True):
  """Please use `jax.shard_map`. `jax.experimental.shard_map.shard_map`
  has been deprecated."""
  return jshmap._shard_map(f, mesh=mesh, in_specs=in_specs, out_specs=out_specs,
                           axis_names=set(), check_vma=check_rep)


def shard_map(f: F, /, *, out_specs: Specs,
              in_specs: Specs | None | InferFromArgs = ...,
              mesh: Mesh | AbstractMesh | None = ...,
              axis_names: Set[AxisName] = ..., check_vma: bool = ...) -> F:
  ...


def shard_map(f: None = None, /, *, out_specs: Specs,
              in_specs: Specs | None | InferFromArgs = ...,
              mesh: Mesh | AbstractMesh | None = ...,
              axis_names: Set[AxisName] = ..., check_vma: bool = ...
              ) -> Callable[[G], G]:
  ...


def shard_map(f: F | None = None, /, *, out_specs: Specs,
              in_specs: Specs | None | InferFromArgs = Infer,
              mesh: Mesh | AbstractMesh | None = None,
              axis_names: Set[AxisName] = frozenset(), check_vma: bool = True
              ) -> F | Callable[[G], G]:
  """Map a function over shards of data using a mesh of devices.

  See the docs at https://docs.jax.dev/en/latest/notebooks/shard_map.html.

  Args:
    f: callable to be mapped. Each application of ``f``, or "instance" of ``f``,
      takes as input a shard of the mapped-over arguments and produces a shard
      of the output.
    mesh: (optional, default None) a ``jax.sharding.Mesh`` representing the
      array of devices over which to shard the data and on which to execute
      instances of ``f``. The names of the ``Mesh`` can be used in collective
      communication operations in ``f``. If mesh is None, it will be inferred
      from the context which can be set via `jax.set_mesh` context
      manager.
    in_specs: (optional, default `Infer`) a pytree with
      ``jax.sharding.PartitionSpec`` instances as leaves, with a tree structure
      that is a tree prefix of the args tuple to be mapped over. Similar to
      ``jax.sharding.NamedSharding``, each ``PartitionSpec`` represents how the
      corresponding argument (or subtree of arguments) should be sharded along
      the named axes of ``mesh``. In each ``PartitionSpec``, mentioning a
      ``mesh`` axis name at a position expresses sharding the corresponding
      argument array axis along that positional axis; not mentioning an axis
      name expresses replication.
      If ``Infer``, all mesh axes must be of type
      `Explicit`, in which case the in_specs are inferred from the argument types.
      If ``None``, inputs will be treated as static.
    out_specs: a pytree with ``PartitionSpec`` instances as leaves, with a tree
      structure that is a tree prefix of the output of ``f``. Each
      ``PartitionSpec`` represents how the corresponding output shards should be
      concatenated. In each ``PartitionSpec``, mentioning a ``mesh`` axis name
      at a position expresses concatenation of that mesh axis's shards along the
      corresponding positional axis; not mentioning a ``mesh`` axis name
      expresses a promise that the output values are equal along that mesh axis,
      and that rather than concatenating only a single value should be produced.
    axis_names: (optional, default set()) set of axis names from ``mesh`` over
      which the function ``f`` is manual. If empty, ``f``, is manual
      over all mesh axes.
    check_vma: (optional) boolean (default True) representing whether to enable
      additional validity checks and automatic differentiation optimizations.
      The validity checks concern whether any mesh axis names not mentioned in
      ``out_specs`` are consistent with how the outputs of ``f`` are replicated.

  Returns:
    A callable representing a mapped version of ``f``, which accepts positional
    arguments corresponding to those of ``f`` and produces output corresponding
    to that of ``f``.
  """
  kwargs = dict(mesh=mesh, in_specs=in_specs, out_specs=out_specs,
                axis_names=axis_names, check_vma=check_vma)
  if f is None:
    return lambda g: _shard_map(g, **kwargs)
  return _shard_map(f, **kwargs)


def shard_map(
    f: F,
    *,
    mesh: Mesh | AbstractMesh,
    in_specs: Specs,
    out_specs: Specs,
    axis_names: tp.AbstractSet[AxisName] = frozenset(),
    check_vma: bool = True,
    graph: bool | None = None,
    graph_updates: bool | None = None,
) -> F:
  ...


def shard_map(
    *,
    mesh: Mesh | AbstractMesh,
    in_specs: Specs,
    out_specs: Specs,
    axis_names: tp.AbstractSet[AxisName] = frozenset(),
    check_vma: bool = True,
    graph: bool | None = None,
    graph_updates: bool | None = None,
) -> tp.Callable[[F], F]:
  ...


def shard_map(
    f: F | type[Missing] = Missing,
    *,
    mesh: Mesh | AbstractMesh,
    in_specs: Specs,
    out_specs: Specs,
    axis_names: tp.AbstractSet[AxisName] = frozenset(),
    check_vma: bool = True,
    graph: bool | None = None,
    graph_updates: bool | None = None,
) -> F | tp.Callable[[F], F]:
  """
  Lifted version of
  `jax.shard_map <https://docs.jax.dev/en/latest/_autosummary/jax.shard_map.html>`_
  that can handle Modules / graph nodes as arguments.

  Simple data parallel example::

    import jax
    import jax.numpy as jnp
    from flax import nnx
    from jax.sharding import PartitionSpec as P

    mesh = jax.sharding.Mesh(jax.local_devices(), ('data',))

    m = nnx.Linear(2, 3, rngs=nnx.Rngs(0))
    x = jnp.ones((32, 2))

    @nnx.shard_map(
      mesh=mesh, in_specs=(P(None), P('data')), out_specs=P('data')
    )
    def f(m, x):
      return m(x)

    y = f(m, x)

    jax.debug.visualize_array_sharding(y)

  Notice that here we simply used some ``PartitionSpec`` to define the spec
  the whole model and data. This works for simple cases but if we need
  to assign different ``PartitionSpec`` to different parts of the model we
  need to use ``StateSharding`` and create some filters that allow us to target
  specific parts of the model. Here's an example of how to do tensor parallelism
  for a simple MLP block using ``StateSharding`` and filters::

    mesh = jax.sharding.Mesh(jax.local_devices(), ('model',))

    class MLP(nnx.Module):
      def __init__(self, din, dhidden, dout, *, rngs: nnx.Rngs):
        self.linear1 = nnx.Linear(din, dhidden, use_bias=False, rngs=rngs)
        self.linear2 = nnx.Linear(dhidden, dout, use_bias=False, rngs=rngs)

      def __call__(self, x):
        return self.linear2(jax.nn.relu(self.linear1(x)))

    m = MLP(2, 64, 3, rngs=nnx.Rngs(0))
    x = jnp.ones((32, 2))

    def path_ends_with(*path_suffix): # custom filter
      return lambda path, value: path[-len(path_suffix):] == path_suffix

    model_spec = nnx.StateSharding({
      path_ends_with('linear1', 'kernel'): P(None, 'model'),
      path_ends_with('linear2', 'kernel'): P('model', None),
    })

    @nnx.shard_map(mesh=mesh, in_specs=(model_spec, P(None)), out_specs=P(None))
    def f(m, x):
      y = m(x)
      return jax.lax.psum(y, 'model')

    y = f(m, x)

    jax.debug.visualize_array_sharding(m.linear1.kernel[...])
    jax.debug.visualize_array_sharding(m.linear2.kernel[...])


  Alternatively, a ``State`` object with the exact PartitionSpec for each
  state then you can be passed to ``StateSharding``::

    mesh = jax.sharding.Mesh(jax.local_devices(), ('model',))

    class MLP(nnx.Module):
      def __init__(self, din, dhidden, dout, *, rngs: nnx.Rngs):
        self.linear1 = nnx.Linear(din, dhidden, use_bias=False, rngs=rngs)
        self.linear2 = nnx.Linear(dhidden, dout, use_bias=False, rngs=rngs)

      def __call__(self, x):
        return self.linear2(jax.nn.relu(self.linear1(x)))

    m = MLP(2, 64, 3, rngs=nnx.Rngs(0))
    x = jnp.ones((32, 2))

    model_spec = nnx.State(
      {
        'linear1': {'kernel': P(None, 'model')},
        'linear2': {'kernel': P('model', None)},
      }
    )

    @nnx.shard_map(
      mesh=mesh,
      in_specs=(nnx.StateSharding(model_spec), P(None)),
      out_specs=P(None),
    )
    def f(m, x):
      y = m(x)
      return jax.lax.psum(y, 'model')

    y = f(m, x)

    jax.debug.visualize_array_sharding(m.linear1.kernel[...])
    jax.debug.visualize_array_sharding(m.linear2.kernel[...])

  Here ``model_spec`` was created manually but you can also automate
  this process by using ``nnx.get_partition_spec`` to automatically
  create it for you (see
  `Scale up on multiple devices <https://flax.readthedocs.io/en/latest/guides/flax_gspmd.html>`_
  ).

  Args:
    f: callable to be mapped. Each application of ``f``, or "instance" of ``f``,
      takes as input a shard of the mapped-over arguments and produces a shard
      of the output.
    mesh: a ``jax.sharding.Mesh`` representing the array of devices over which
      to shard the data and on which to execute instances of ``f``. The names of
      the ``Mesh`` can be used in collective communication operations in ``f``.
      This is typically created by a utility function like
      :func:`jax.experimental.mesh_utils.create_device_mesh`.
    in_specs: a pytree with ``jax.sharding.PartitionSpec``or ``nnx.StateSharding``
      (mapping substates to ``PartitionSpec``s) instances as leaves,
      with a tree structure that is a tree prefix of the
      args tuple to be mapped over. Similar to ``jax.sharding.NamedSharding``,
      each ``PartitionSpec`` represents how the corresponding argument (or subtree
      of arguments) should be sharded along the named axes of ``mesh``. In each
      ``PartitionSpec``, mentioning a ``mesh`` axis name at a position expresses sharding
      the corresponding argument array axis along that positional axis; not
      mentioning an axis name expresses replication. If an argument, or argument
      subtree, has a corresponding spec of None, that argument is not sharded.
    out_specs: a pytree with ``jax.sharding.PartitionSpec`` or ``nnx.StateSharding``
      (mapping substates to ``PartitionSpec``s) instances as leaves, with a tree structure
      that is a tree prefix of the output of ``f``.
      Each ``PartitionSpec`` represents how the corresponding output shards should be
      concatenated. In each ``PartitionSpec``, metioning a ``mesh`` axis name at
      a position expresses concatenation of that mesh axis's shards along the
      corresponding positional axis. Not mentioning a ``mesh`` axis name
      expresses a promise that the output values are equal along that mesh axis,
      and that rather than concatenating only a single value should be produced.
    axis_names: optional set of axis names from ``mesh`` over which the function ``f``
      is manual. If empty, ``f``, is manual over all mesh axes.
    check_vma: optional boolean representing whether to enable additional validity
      checks and automatic differentiation optimizations. The validity checks concern
      whether any mesh axis names not mentioned in ``out_specs`` are consistent with
      how the outputs of ``f`` are replicated.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references and reference semantics.
      If ``False``, uses tree-mode which treats Modules as regular JAX
      pytrees, avoiding the overhead of the graph protocol. Tree-mode does
      not support ``StateSharding`` or shared ``Variable`` references.
    graph_updates: If ``True``, propagates updates on graph structure
      that happen inside the transform to the input graphs, has no
      effect when ``graph=False``. When ``False``, using
      ``StateSharding`` is not supported.

  Returns:
    A callable that applies the input function ``f`` across data sharded according to
    the ``mesh`` and ``in_specs``.
  """
  if graph is None:
    graph = graphlib.set_graph_mode.current_value()
  if graph_updates is None:
    graph_updates = graphlib.set_graph_updates.current_value()
  if f is Missing:
    return functools.partial(
        shard_map,
        mesh=mesh,
        in_specs=in_specs,
        out_specs=out_specs,
        axis_names=axis_names,
        check_vma=check_vma,
        graph=graph,
        graph_updates=graph_updates,
    )  # type: ignore[return-value]
  assert not isinstance(f, type)

  f_unbound, _, was_bound = _resolve_bound_callable(f)
  if was_bound:
    _raise_bound_method_error('shard_map')

  extract.check_prefix(
    in_specs, 'in_specs', 'shard_map', graph, graph_updates
  )
  extract.check_prefix(
    out_specs, 'out_specs', 'shard_map', graph, graph_updates
  )

  if not (graph and graph_updates):

    shard_map_fn = jax.shard_map(
        SimpleShardMapFn(f_unbound, graph=graph, out_specs=out_specs),
        mesh=mesh,
        in_specs=in_specs,
        out_specs=(out_specs, in_specs),
        axis_names=axis_names,
        check_vma=check_vma,
    )

    @functools.wraps(f)
    def shard_map_wrapper(*args, **kwargs):
      if graph:
        args = extract.to_tree2(
            args,
            prefix=in_specs,
            check_aliasing=in_specs is not None,
        )
      extract.check_no_aliases('shard_map', args=args)
      out, updates = shard_map_fn(*args, **kwargs)
      extract.apply_variable_updates(args, updates)
      if graph:
        out = extract.from_tree2(out)
      return out

    shard_map_wrapper.inner = shard_map_fn  # type: ignore
    return shard_map_wrapper  # type: ignore

  kwarg_specs = PartitionSpec()
  jax_in_specs = jax.tree.map(
    lambda x: extract.NodeStates(
      _graphdef=PartitionSpec(),  # type: ignore[arg-type]
      states=x.shardings,
      metadata=x,
    )
    if isinstance(x, StateSharding)
    else x,
    in_specs,
  )
  jax_out_specs = jax.tree.map(
    lambda x: extract.NodeStates(
      _graphdef=PartitionSpec(),  # type: ignore[arg-type]
      states=x.shardings,
      metadata=x,
    )
    if isinstance(x, StateSharding)
    else x,
    out_specs,
  )

  @functools.wraps(f)  # type: ignore[no-redef]
  def shard_map_wrapper(*args, **kwargs):
    with graphlib.update_context(shard_map_wrapper):
      pure_args, pure_kwargs = extract.to_tree(
        (args, kwargs),
        prefix=(in_specs, kwarg_specs)
        if in_specs is not None or kwarg_specs is not None
        else None,
        split_fn=_jit_split_fn,
        check_aliasing=in_specs is not None or kwarg_specs is not None,
        ctxtag=shard_map_wrapper,
      )
      pure_args_out, pure_kwargs_out, pure_out = shard_map_fn(
        *pure_args, **pure_kwargs
      )
      _args_out, _kwargs_out, out = extract.from_tree(
        (pure_args_out, pure_kwargs_out, pure_out),
        merge_fn=_jit_merge_fn,
        is_inner=False,
        ctxtag=shard_map_wrapper,
      )
    return out

  shard_map_fn = jax.shard_map(
      ShardMapFn(f_unbound, in_specs, out_specs, kwarg_specs, shard_map_wrapper),
      mesh=mesh,
      in_specs=jax_in_specs,
      out_specs=(jax_in_specs, kwarg_specs, jax_out_specs),  # type: ignore
      axis_names=axis_names,
      check_vma=check_vma,
  )

  shard_map_wrapper.inner = shard_map_fn  # type: ignore

  return shard_map_wrapper  # type: ignore

