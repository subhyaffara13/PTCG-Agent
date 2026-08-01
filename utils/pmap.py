
def pmap(
    fun: Callable,
    axis_name: AxisName | None = None,
    *,
    in_axes: int | None | Sequence[Any] = 0,
    out_axes: Any = 0,
    static_broadcasted_argnums: int | Iterable[int] = (),
    devices: Sequence[xc.Device] | None = None,  # noqa: F811
    backend: str | None = None,
    axis_size: int | None = None,
    donate_argnums: int | Iterable[int] = (),
  ) -> Any:
  """Old way of doing parallel map. Use :py:func:`jax.shard_map` instead.

  .. note::
    While :py:func:`jax.pmap` works, you should probably use
    :py:func:`jax.shard_map` or ``jax.smap`` instead. shard_map supports more
    efficient autodiff, and is more composable in the multi-controller setting.
    See https://docs.jax.dev/en/latest/notebooks/shard_map.html for examples.

  .. note::
    :py:func:`pmap` is now implemented in terms of :py:func:`jit` and
    :py:func:`shard_map`. Please see the `migration
    guide <https://docs.jax.dev/en/latest/migrate_pmap.html>`_ for
    more information.

  The purpose of :py:func:`pmap` is to express single-program multiple-data
  (SPMD) programs. Applying :py:func:`pmap` to a function will compile the
  function with XLA (similarly to :py:func:`jit`), then execute it in parallel
  on XLA devices, such as multiple GPUs or multiple TPU cores. Semantically it
  is comparable to :py:func:`vmap` because both transformations map a function
  over array axes, but where :py:func:`vmap` vectorizes functions by pushing the
  mapped axis down into primitive operations, :py:func:`pmap` instead replicates
  the function and executes each replica on its own XLA device in parallel.

  The mapped axis size must be less than or equal to the number of local XLA
  devices available, as returned by :py:func:`jax.local_device_count()` (unless
  ``devices`` is specified, see below). For nested :py:func:`pmap` calls, the
  product of the mapped axis sizes must be less than or equal to the number of
  XLA devices.

  .. note::
    :py:func:`pmap` compiles ``fun``, so while it can be combined with
    :py:func:`jit`, it's usually unnecessary.

  :py:func:`pmap` requires that all of the participating devices are identical.
  For example, it is not possible to use :py:func:`pmap` to parallelize a
  computation across two different models of GPU. It is currently an error for
  the same device to participate twice in the same `pmap`.

  **Multi-process platforms:** On multi-process platforms such as TPU pods,
  :py:func:`pmap` is designed to be used in SPMD Python programs, where every
  process is running the same Python code such that all processes run the same
  pmapped function in the same order. Each process should still call the pmapped
  function with mapped axis size equal to the number of *local* devices (unless
  ``devices`` is specified, see below), and an array of the same leading axis
  size will be returned as usual. However, any collective operations in ``fun``
  will be computed over *all* participating devices, including those on other
  processes, via device-to-device communication.  Conceptually, this can be
  thought of as running a pmap over a single array sharded across processes,
  where each process "sees" only its local shard of the input and output. The
  SPMD model requires that the same multi-process pmaps must be run in the same
  order on all devices, but they can be interspersed with arbitrary operations
  running in a single process.

  Args:
    fun: Function to be mapped over argument axes. Its arguments and return
      value should be arrays, scalars, or (nested) standard Python containers
      (tuple/list/dict) thereof. Positional arguments indicated by
      ``static_broadcasted_argnums`` can be anything at all, provided they are
      hashable and have an equality operation defined.
    axis_name: Optional, a hashable Python object used to identify the mapped
      axis so that parallel collectives can be applied.
    in_axes: A non-negative integer, None, or nested Python container thereof
      that specifies which axes of positional arguments to map over. Arguments
      passed as keywords are always mapped over their leading axis (i.e. axis
      index 0). See :py:func:`vmap` for details.
    out_axes: A non-negative integer, None, or nested Python container thereof
      indicating where the mapped axis should appear in the output. All outputs
      with a mapped axis must have a non-None ``out_axes`` specification
      (see :py:func:`vmap`).
    static_broadcasted_argnums: An int or collection of ints specifying which
      positional arguments to treat as static (compile-time constant).
      Operations that only depend on static arguments will be constant-folded.
      Calling the pmapped function with different values for these constants
      will trigger recompilation. If the pmapped function is called with fewer
      positional arguments than indicated by ``static_broadcasted_argnums`` then
      an error is raised. Each of the static arguments will be broadcasted to
      all devices. Arguments that are not arrays or containers thereof must be
      marked as static. Defaults to ().

      Static arguments must be hashable, meaning both ``__hash__`` and
      ``__eq__`` are implemented, and should be immutable.

    devices: This is an experimental feature and the API is likely to change.
      Optional, a sequence of Devices to map over. (Available devices can be
      retrieved via jax.devices()). Must be given identically for each process
      in multi-process settings (and will therefore include devices across
      processes). If specified, the size of the mapped axis must be equal to
      the number of devices in the sequence local to the given process. Nested
      :py:func:`pmap` s with ``devices`` specified in either the inner or outer
      :py:func:`pmap` are not yet supported.
    backend: This is an experimental feature and the API is likely to change.
      Optional, a string representing the XLA backend. 'cpu', 'gpu', or 'tpu'.
    axis_size: Optional; the size of the mapped axis.
    donate_argnums: Specify which positional argument buffers are "donated" to
      the computation. It is safe to donate argument buffers if you no longer need
      them once the computation has finished. In some cases XLA can make use of
      donated buffers to reduce the amount of memory needed to perform a
      computation, for example recycling one of your input buffers to store a
      result. You should not reuse buffers that you donate to a computation, JAX
      will raise an error if you try to.
      Note that donate_argnums only work for positional arguments, and keyword
      arguments will not be donated.

      For more details on buffer donation see the
      `FAQ <https://docs.jax.dev/en/latest/faq.html#buffer-donation>`_.

  Returns:
    A parallelized version of ``fun`` with arguments that correspond to those of
    ``fun`` but with extra array axes at positions indicated by ``in_axes`` and
    with output that has an additional leading array axis (with the same size).

  For example, assuming 8 XLA devices are available, :py:func:`pmap` can be used
  as a map along a leading array axis:

  >>> import jax.numpy as jnp
  >>>
  >>> out = pmap(lambda x: x ** 2)(jnp.arange(8))  # doctest: +SKIP
  >>> print(out)  # doctest: +SKIP
  [0, 1, 4, 9, 16, 25, 36, 49]

  When the leading dimension is smaller than the number of available devices JAX
  will simply run on a subset of devices:

  >>> x = jnp.arange(3 * 2 * 2.).reshape((3, 2, 2))
  >>> y = jnp.arange(3 * 2 * 2.).reshape((3, 2, 2)) ** 2
  >>> out = pmap(jnp.dot)(x, y)  # doctest: +SKIP
  >>> print(out)  # doctest: +SKIP
  [[[    4.     9.]
    [   12.    29.]]
   [[  244.   345.]
    [  348.   493.]]
   [[ 1412.  1737.]
    [ 1740.  2141.]]]

  If your leading dimension is larger than the number of available devices you
  will get an error:

  >>> pmap(lambda x: x ** 2)(jnp.arange(9))  # doctest: +SKIP
  ValueError: ... requires 9 replicas, but only 8 XLA devices are available

  As with :py:func:`vmap`, using ``None`` in ``in_axes`` indicates that an
  argument doesn't have an extra axis and should be broadcasted, rather than
  mapped, across the replicas:

  >>> x, y = jnp.arange(2.), 4.
  >>> out = pmap(lambda x, y: (x + y, y * 2.), in_axes=(0, None))(x, y)  # doctest: +SKIP
  >>> print(out)  # doctest: +SKIP
  ([4., 5.], [8., 8.])

  Note that :py:func:`pmap` always returns values mapped over their leading axis,
  equivalent to using ``out_axes=0`` in :py:func:`vmap`.

  In addition to expressing pure maps, :py:func:`pmap` can also be used to express
  parallel single-program multiple-data (SPMD) programs that communicate via
  collective operations. For example:

  >>> f = lambda x: x / jax.lax.psum(x, axis_name='i')
  >>> out = pmap(f, axis_name='i')(jnp.arange(4.))  # doctest: +SKIP
  >>> print(out)  # doctest: +SKIP
  [ 0.          0.16666667  0.33333334  0.5       ]
  >>> print(out.sum())  # doctest: +SKIP
  1.0

  In this example, ``axis_name`` is a string, but it can be any Python object
  with ``__hash__`` and ``__eq__`` defined.

  The argument ``axis_name`` to :py:func:`pmap` names the mapped axis so that
  collective operations, like :func:`jax.lax.psum`, can refer to it. Axis names
  are important particularly in the case of nested :py:func:`pmap` functions,
  where collective operations can operate over distinct axes:

  On multi-process platforms, collective operations operate over all devices,
  including those on other processes. For example, assuming the following code
  runs on two processes with 4 XLA devices each:

  >>> f = lambda x: x + jax.lax.psum(x, axis_name='i')
  >>> data = jnp.arange(4) if jax.process_index() == 0 else jnp.arange(4, 8)
  >>> out = pmap(f, axis_name='i')(data)  # doctest: +SKIP
  >>> print(out)  # doctest: +SKIP
  [28 29 30 31] # on process 0
  [32 33 34 35] # on process 1

  Each process passes in a different length-4 array, corresponding to its 4
  local devices, and the psum operates over all 8 values. Conceptually, the two
  length-4 arrays can be thought of as a sharded length-8 array (in this example
  equivalent to jnp.arange(8)) that is mapped over, with the length-8 mapped
  axis given name 'i'. The pmap call on each process then returns the
  corresponding length-4 output shard.

  The ``devices`` argument can be used to specify exactly which devices are used
  to run the parallel computation. For example, again assuming a single process
  with 8 devices, the following code defines two parallel computations, one
  which runs on the first six devices and one on the remaining two:

  >>> from functools import partial
  >>> @partial(pmap, axis_name='i', devices=jax.devices()[:6])
  ... def f1(x):
  ...   return x / jax.lax.psum(x, axis_name='i')
  >>>
  >>> @partial(pmap, axis_name='i', devices=jax.devices()[-2:])
  ... def f2(x):
  ...   return jax.lax.psum(x ** 2, axis_name='i')
  >>>
  >>> print(f1(jnp.arange(6.)))  # doctest: +SKIP
  [0.         0.06666667 0.13333333 0.2        0.26666667 0.33333333]
  >>> print(f2(jnp.array([2., 3.])))  # doctest: +SKIP
  [ 13.  13.]
  """
  if devices is not None:
    if not devices:
      raise ValueError("'devices' argument to pmap must be non-empty, or None.")
    devices = tuple(devices)
  axis_name, static_broadcasted_tuple, donate_tuple = _prepare_pmap(
      fun, axis_name, static_broadcasted_argnums, donate_argnums, in_axes,
      out_axes)
  wrapped_fun = _pmap_wrap_init(fun, static_broadcasted_tuple)
  out_axes_flat, out_axes_tree = tree_flatten(out_axes)
  out_axes_flat = tuple(out_axes_flat)

  def infer_params(*args, **kwargs):
    process_count = xb.process_count(backend)
    trace_state_clean = core.trace_state_clean()
    dyn_f, dyn_argnums, dyn_args = _get_dyn_args(
        wrapped_fun, static_broadcasted_tuple, args)
    dyn_args_flat, dyn_args_tree = tree_flatten((dyn_args, kwargs))
    in_axes_flat = _get_in_axes_flat(
        in_axes, dyn_argnums, dyn_args, kwargs, len(dyn_args_flat),
        dyn_args_tree)
    local_axis_size = _mapped_axis_size(dyn_args_flat, in_axes_flat)
    donated_invars = _get_donated_invars(
        donate_tuple, dyn_args_tree, len(dyn_args_flat))
    mesh_devices = _get_mesh_devices(
        devices, backend, local_axis_size, axis_size, trace_state_clean)
    cached = _cached_shard_map(
        dyn_f, dyn_args_tree, in_axes_flat, out_axes_flat, out_axes_tree,
        donated_invars, mesh_devices, axis_name)
    jitted_f = (cached.jitted_f_with_shardings if trace_state_clean
                else cached.jitted_f)
    if process_count > 1:
      dyn_args_flat = host_local_array_to_global_array(
          dyn_args_flat, cached, trace_state_clean, donated_invars
      )
    return (cached, jitted_f, dyn_args_flat, dyn_args_tree, donate_tuple,
            process_count, trace_state_clean)

  @util.wraps(fun)
  def wrapped(*args, **kwargs):
    cached, jitted_f, dyn_args_flat, _, _, process_count, trace_state_clean = (
        infer_params(*args, **kwargs))
    out = jitted_f(*dyn_args_flat)
    if process_count > 1:
      out = global_array_to_host_local_array(out, cached, trace_state_clean)
    return out

  def lower(*args, **kwargs):
    _, jitted_f, args_flat, in_tree, donated_tuple, _, _ = infer_params(
        *args, **kwargs
    )
    abstract_args = list(map(core.shaped_abstractify, args_flat))
    args_info = stages.make_args_info(in_tree, abstract_args, donated_tuple)
    lowered = jitted_f.trace(*args_flat).lower()
    # NOTE(dsuo): Calling .compile()(*inputs) will fail because our jitted function
    # has no notion of host-local <> global conversion.
    return stages.Lowered(
        lowered._lowering,
        args_info,
        lowered.out_tree,
        no_kwargs=lowered._no_kwargs,
    )

  wrapped.lower = lower  # pyrefly: ignore[missing-attribute]
  return wrapped


def pmap(
    *,
    axis_name: AxisName | None = None,
    in_axes: tp.Any = 0,
    out_axes: tp.Any = 0,
    static_broadcasted_argnums: int | tp.Iterable[int] = (),
    devices: tp.Sequence[jax.Device] | None = None,  # noqa: F811
    backend: str | None = None,
    axis_size: int | None = None,
    donate_argnums: int | tp.Iterable[int] = (),
    # nnx specific
    transform_metadata: tp.Mapping[str, tp.Any] = FrozenDict({}),
    graph: bool | None = None,
    graph_updates: bool | None = None,
) -> tp.Callable[[F], F]:
  ...


def pmap(
    f: F,
    *,
    axis_name: AxisName | None = None,
    in_axes: tp.Any = 0,
    out_axes: tp.Any = 0,
    static_broadcasted_argnums: int | tp.Iterable[int] = (),
    devices: tp.Sequence[jax.Device] | None = None,  # noqa: F811
    backend: str | None = None,
    axis_size: int | None = None,
    donate_argnums: int | tp.Iterable[int] = (),
    # nnx specific
    transform_metadata: tp.Mapping[str, tp.Any] = FrozenDict({}),
    graph: bool | None = None,
    graph_updates: bool | None = None,
) -> F:
  ...


def pmap(
  f: F | type[Missing] = Missing,
  *,
  axis_name: AxisName | None = None,
  in_axes: tp.Any = 0,
  out_axes: tp.Any = 0,
  static_broadcasted_argnums: int | tp.Iterable[int] = (),
  devices: tp.Sequence[jax.Device] | None = None,  # noqa: F811
  backend: str | None = None,
  axis_size: int | None = None,
  donate_argnums: int | tp.Iterable[int] = (),
  # nnx specific
  transform_metadata: tp.Mapping[str, tp.Any] = FrozenDict({}),
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> F | tp.Callable[[F], F]:
  """Reference-aware version of `jax.pmap <https://jax.readthedocs.io/en/latest/_autosummary/jax.pmap.html>`__.

  Args:
    f: Function to be mapped over argument axes. Its arguments and return
      value should be arrays, scalars, graph nodes, or (nested) standard
      Python containers (tuple/list/dict) thereof. Positional arguments
      indicated by ``static_broadcasted_argnums`` can be anything at all,
      provided they are hashable and have an equality operation defined.
    axis_name: Optional, a hashable Python object used to identify the mapped
      axis so that parallel collectives can be applied.
    in_axes: A non-negative integer, None, or nested Python container thereof
      that specifies which axes of positional arguments to map over. Arguments
      passed as keywords are always mapped over their leading axis (i.e. axis
      index 0). In addition to integers and None, :class:`StateAxes` can be
      used to control how graph nodes like Modules are vectorized by specifying
      the axes to be applied to substates of the graph node given a `Filter
      <https://flax.readthedocs.io/en/latest/guides/filters_guide.html>`__.
    out_axes: A non-negative integer, None, or nested Python container thereof
      indicating where the mapped axis should appear in the output. All outputs
      with a mapped axis must have a non-None ``out_axes`` specification.
    static_broadcasted_argnums: An int or collection of ints specifying which
      positional arguments to treat as static (compile-time constant).
      Operations that only depend on static arguments will be constant-folded.
      Calling the pmapped function with different values for these constants
      will trigger recompilation. If the pmapped function is called with fewer
      positional arguments than indicated by ``static_broadcasted_argnums`` then
      an error is raised. Each of the static arguments will be broadcasted to
      all devices. Arguments that are not arrays or containers thereof must be
      marked as static. Defaults to ().
      Static arguments must be hashable, meaning both ``__hash__`` and
      ``__eq__`` are implemented, and should be immutable.
    devices: This is an experimental feature and the API is likely to change.
      Optional, a sequence of Devices to map over. (Available devices can be
      retrieved via jax.devices()). Must be given identically for each process
      in multi-process settings (and will therefore include devices across
      processes). If specified, the size of the mapped axis must be equal to
      the number of devices in the sequence local to the given process. Nested
      ``pmap`` s with ``devices`` specified in either the inner or outer
      ``pmap`` are not yet supported.
    backend: This is an experimental feature and the API is likely to change.
      Optional, a string representing the XLA backend. 'cpu', 'gpu', or 'tpu'.
    axis_size: Optional; the size of the mapped axis.
    donate_argnums: Specify which positional argument buffers are "donated" to
      the computation. It is safe to donate argument buffers if you no longer
      need them once the computation has finished. In some cases XLA can make
      use of donated buffers to reduce the amount of memory needed to perform a
      computation, for example recycling one of your input buffers to store a
      result. You should not reuse buffers that you donate to a computation,
      JAX will raise an error if you try to. Note that donate_argnums only
      work for positional arguments, and keyword arguments will not be donated.
    transform_metadata: Optional mapping of metadata for the transform.
    graph: if True, use graph-mode (default). If False, use tree-mode.
      If None, uses the value of ``nnx_graph_mode`` config.
    graph_updates: If ``True``, propagates updates on graph structure
      that happen inside the transform to the input graphs, has no
      effect when ``graph=False``. When ``False``, using ``StateAxes``
      is not supported.

  Returns:
    A parallelized version of ``f`` with arguments that correspond to those of
    ``f`` but with extra array axes at positions indicated by ``in_axes`` and
    with output that has an additional leading array axis (with the same size).
  """
  if graph is None:
    graph = graphlib.set_graph_mode.current_value()
  if graph_updates is None:
    graph_updates = graphlib.set_graph_updates.current_value()
  if f is Missing:
    return functools.partial(
        pmap,
        axis_name=axis_name,
        in_axes=in_axes,
        out_axes=out_axes,
        static_broadcasted_argnums=static_broadcasted_argnums,
        devices=devices,
        backend=backend,
        axis_size=axis_size,
        donate_argnums=donate_argnums,
        transform_metadata=transform_metadata,
        graph=graph,
        graph_updates=graph_updates,
    )  # type: ignore[return-value]

  f_unbound, _, was_bound = _resolve_bound_callable(f)
  if was_bound:
    _raise_bound_method_error('pmap')

  extract.check_prefix(in_axes, 'in_axes', 'pmap', graph, graph_updates)
  extract.check_prefix(out_axes, 'out_axes', 'pmap', graph, graph_updates)

  if not (graph and graph_updates):

    pmapped_fn = jax.pmap(
      SimplePmapFn(f_unbound, graph=graph, out_axes=out_axes),
      axis_name=axis_name,
      in_axes=in_axes,
      out_axes=(out_axes, (in_axes, 0)),
      static_broadcasted_argnums=static_broadcasted_argnums,
      devices=devices,
      backend=backend,
      axis_size=axis_size,
      donate_argnums=donate_argnums,
    )

    @functools.wraps(f_unbound)
    def simple_pmap_wrapper(*args, **kwargs):
      if graph:
        args, kwargs = extract.to_tree2(
            (args, kwargs),
            prefix=(in_axes, None)
            if in_axes is not None
            else None,
            check_aliasing=in_axes is not None,
        )
      extract.check_no_aliases('pmap', args=args, kwargs=kwargs)
      out, updates = pmapped_fn(*args, **kwargs)
      extract.apply_variable_updates((args, kwargs), updates)
      if graph:
        out = extract.from_tree2(out)
      return out

    return simple_pmap_wrapper  # type: ignore[return-value]

  jax_in_axes = jax.tree.map(
    lambda x: extract.NodeStates.from_prefixes(x.axes, metadata=x)
    if isinstance(x, StateAxes)
    else x,
    in_axes,
  )
  jax_out_axes = jax.tree.map(
    lambda x: extract.NodeStates.from_prefixes(x.axes, metadata=x)
    if isinstance(x, StateAxes)
    else x,
    out_axes,
  )
  pmapped_fn = jax.pmap(
      PmapFn(f_unbound, transform_metadata, in_axes, out_axes),
      axis_name=axis_name,
      in_axes=jax_in_axes,
      out_axes=(jax_in_axes, jax_out_axes),
      static_broadcasted_argnums=static_broadcasted_argnums,
      devices=devices,
      backend=backend,
      axis_size=axis_size,
      donate_argnums=donate_argnums,
  )

  @functools.wraps(f)
  @graphlib.update_context('pmap')
  def vmap_wrapper(*args):
    pure_args = extract.to_tree(
        args, prefix=in_axes, split_fn=_vmap_split_fn, ctxtag='pmap'
    )
    pure_args_out, pure_out = pmapped_fn(*pure_args)
    _args_out, out = extract.from_tree(
      (pure_args_out, pure_out), ctxtag='pmap', is_inner=False
    )
    return out

  return vmap_wrapper  # type: ignore

