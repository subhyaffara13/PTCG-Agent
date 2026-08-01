
def jit(
  fun: Callable, /, *,
  in_shardings: Any = ...,
  out_shardings: Any = ...,
  static_argnums: int | Sequence[int] | None = ...,
  static_argnames: str | Iterable[str] | None = ...,
  donate_argnums: int | Sequence[int] | None = ...,
  donate_argnames: str | Iterable[str] | None = ...,
  keep_unused: bool = ...,
  device: xc.Device | None = ...,
  backend: str | None = ...,
  inline: bool = ...,
  compiler_options: dict[str, Any] | None = ...,
) -> pjit.JitWrapped:
  ...


def jit(
  *,
  in_shardings: Any = ...,
  out_shardings: Any = ...,
  static_argnums: int | Sequence[int] | None = ...,
  static_argnames: str | Iterable[str] | None = ...,
  donate_argnums: int | Sequence[int] | None = ...,
  donate_argnames: str | Iterable[str] | None = ...,
  keep_unused: bool = ...,
  device: xc.Device | None = ...,
  backend: str | None = ...,
  inline: bool = ...,
  compiler_options: dict[str, Any] | None = ...,
) -> Callable[[Callable], pjit.JitWrapped]:
  ...


def jit(
  fun: Callable | NotSpecified = NotSpecified(), /, *,
  in_shardings: Any = sharding_impls.UNSPECIFIED,
  out_shardings: Any = sharding_impls.UNSPECIFIED,
  static_argnums: int | Sequence[int] | None = None,
  static_argnames: str | Iterable[str] | None = None,
  donate_argnums: int | Sequence[int] | None = None,
  donate_argnames: str | Iterable[str] | None = None,
  keep_unused: bool = False,
  device: xc.Device | None = None,
  backend: str | None = None,
  inline: bool = False,
  compiler_options: dict[str, Any] | None = None,
) -> pjit.JitWrapped | Callable[[Callable], pjit.JitWrapped]:
  """Sets up ``fun`` for just-in-time compilation with XLA.

  Args:
    fun: Function to be jitted. ``fun`` should be a pure function.
      The arguments and return value of ``fun`` should be arrays, scalar, or
      (nested) standard Python containers (tuple/list/dict) thereof. Positional
      arguments indicated by ``static_argnums`` can be any hashable type. Static
      arguments are included as part of a compilation cache key, which is why
      hash and equality operators must be defined. JAX keeps a weak reference to
      ``fun`` for use as a compilation cache key, so the object ``fun`` must be
      weakly-referenceable. Starting in JAX v0.8.1, when ``fun`` is omitted,
      the return value will be a partially-evaluated function to allow the
      decorator factory pattern (see Examples below).
    in_shardings: optional, a :py:class:`Sharding` or pytree with
      :py:class:`Sharding` leaves and structure that is a tree prefix of the
      positional arguments tuple to ``fun``. If provided, the positional
      arguments passed to ``fun`` must have shardings that are compatible with
      ``in_shardings`` or an error is raised, and the compiled computation has
      input shardings corresponding to ``in_shardings``. If not provided, the
      compiled computation's input shardings are inferred from argument
      shardings.
    out_shardings: optional, a :py:class:`Sharding` or pytree with
      :py:class:`Sharding` leaves and structure that is a tree prefix of the
      output of ``fun``. If provided, it has the same effect as applying
      :py:func:`jax.lax.with_sharding_constraint` to the output of ``fun``.
    static_argnums: optional, an int or collection of ints that specify which
      positional arguments to treat as static (trace- and compile-time
      constant).

      Static arguments should be hashable, meaning both ``__hash__`` and
      ``__eq__`` are implemented, and immutable. Otherwise, they can be arbitrary
      Python objects. Calling the jitted function with different values for
      these constants will trigger recompilation. Arguments that are not
      array-like or containers thereof must be marked as static.

      If neither ``static_argnums`` nor ``static_argnames`` is provided, no
      arguments are treated as static. If ``static_argnums`` is not provided but
      ``static_argnames`` is, or vice versa, JAX uses
      :code:`inspect.signature(fun)` to find any positional arguments that
      correspond to ``static_argnames``
      (or vice versa). If both ``static_argnums`` and ``static_argnames`` are
      provided, ``inspect.signature`` is not used, and only actual
      parameters listed in either ``static_argnums`` or ``static_argnames`` will
      be treated as static.
    static_argnames: optional, a string or collection of strings specifying
      which named arguments to treat as static (compile-time constant). See the
      comment on ``static_argnums`` for details. If not
      provided but ``static_argnums`` is set, the default is based on calling
      ``inspect.signature(fun)`` to find corresponding named arguments.
    donate_argnums: optional, collection of integers to specify which positional
      argument buffers can be overwritten by the computation and marked deleted
      in the caller. It is safe to donate argument buffers if you no longer need
      them once the computation has started. In some cases XLA can make use of
      donated buffers to reduce the amount of memory needed to perform a
      computation, for example recycling one of your input buffers to store a
      result. You should not reuse buffers that you donate to a computation; JAX
      will raise an error if you try to. By default, no argument buffers are
      donated.

      If neither ``donate_argnums`` nor ``donate_argnames`` is provided, no
      arguments are donated. If ``donate_argnums`` is not provided but
      ``donate_argnames`` is, or vice versa, JAX uses
      :code:`inspect.signature(fun)` to find any positional arguments that
      correspond to ``donate_argnames``
      (or vice versa). If both ``donate_argnums`` and ``donate_argnames`` are
      provided, ``inspect.signature`` is not used, and only actual
      parameters listed in either ``donate_argnums`` or ``donate_argnames`` will
      be donated.

      For more details on buffer donation see the
      `FAQ <https://docs.jax.dev/en/latest/faq.html#buffer-donation>`_.
    donate_argnames: optional, a string or collection of strings specifying
      which named arguments are donated to the computation. See the
      comment on ``donate_argnums`` for details. If not
      provided but ``donate_argnums`` is set, the default is based on calling
      ``inspect.signature(fun)`` to find corresponding named arguments.
    keep_unused: optional boolean. If `False` (the default), arguments that JAX
      determines to be unused by `fun` *may* be dropped from resulting compiled
      XLA executables. Such arguments will not be transferred to the device nor
      provided to the underlying executable. If `True`, unused arguments will
      not be pruned.
    device: This is an experimental feature and the API is likely to change.
      Optional, the Device the jitted function will run on. (Available devices
      can be retrieved via :py:func:`jax.devices`.) The default is inherited
      from XLA's DeviceAssignment logic and is usually to use
      ``jax.devices()[0]``.
    backend: This is an experimental feature and the API is likely to change.
      Optional, a string representing the XLA backend: ``'cpu'``, ``'gpu'``, or
      ``'tpu'``.
    inline: Optional boolean. Specify whether this function should be inlined
      into enclosing jaxprs. Default False.

  Returns:
    A wrapped version of ``fun``, set up for just-in-time compilation.

  Examples:
    In the following example, ``selu`` can be compiled into a single fused kernel
    by XLA:

    >>> import jax
    >>>
    >>> @jax.jit
    ... def selu(x, alpha=1.67, lmbda=1.05):
    ...   return lmbda * jax.numpy.where(x > 0, x, alpha * jax.numpy.exp(x) - alpha)
    >>>
    >>> key = jax.random.key(0)
    >>> x = jax.random.normal(key, (10,))
    >>> print(selu(x))  # doctest: +SKIP
    [-0.54485  0.27744 -0.29255 -0.91421 -0.62452 -0.24748
    -0.85743 -0.78232  0.76827  0.59566 ]

    Starting in JAX v0.8.1, :func:`jit` supports the decorator factory pattern
    for specifying optional keywords:

    >>> @jax.jit(static_argnames=['n'])
    ... def g(x, n):
    ...   for i in range(n):
    ...     x = x ** 2
    ...   return x
    >>>
    >>> g(jnp.arange(4), 3)
    Array([   0,    1,  256, 6561], dtype=int32)

    For compatiblity with older JAX versions, a common pattern is to use
    :func:`functools.partial`:

    >>> from functools import partial
    >>>
    >>> @partial(jax.jit, static_argnames=['n'])
    ... def g(x, n):
    ...   for i in range(n):
    ...     x = x ** 2
    ...   return x
    >>>
    >>> g(jnp.arange(4), 3)
    Array([   0,    1,  256, 6561], dtype=int32)
  """
  kwds = dict(
      in_shardings=in_shardings, out_shardings=out_shardings,
      static_argnums=static_argnums, static_argnames=static_argnames,
      donate_argnums=donate_argnums, donate_argnames=donate_argnames,
      keep_unused=keep_unused, device=device, backend=backend, inline=inline,
      compiler_options=compiler_options, use_resource_env=False)
  if isinstance(fun, NotSpecified):
    return lambda fun: pjit.make_jit(fun, **kwds)
  else:
    return pjit.make_jit(fun, **kwds)


def jit(
    fn: Callable[..., Any],
    variables: CollectionFilter = True,
    rngs: PRNGSequenceFilter = True,
    static_argnums: int | Iterable[int] = (),
    static_argnames: str | Iterable[str] = (),
    donate_argnums: int | Iterable[int] = (),
    device=None,
    backend: str | None = None,
) -> Callable[..., Any]:
  """Lifted version of ``jax.jit``.

  Args:
    fn: Scope function to be jitted.
    variables: The variable collections that are lifted. By default all
      collections are lifted.
    rngs: The PRNG sequences that are lifted. By default all PRNG sequences
      are lifted.
    static_argnums: An int or collection of ints specifying which positional
      arguments to treat as static (compile-time constant). Operations that only
      depend on static arguments will be constant-folded in Python (during
      tracing), and so the corresponding argument values can be any Python
      object. Static arguments should be hashable, meaning both ``__hash__`` and
      ``__eq__`` are implemented, and immutable. Calling the jitted function
      with different values for these constants will trigger recompilation. If
      the jitted function is called with fewer positional arguments than
      indicated by ``static_argnums`` then an error is raised. Arguments that
      are not arrays or containers thereof must be marked as static.
      Defaults to ().
    static_argnames: An optional string or collection of strings specifying
      which named arguments to treat as static (compile-time constant). See the
      comment on ``static_argnums`` for details. If not
      provided but ``static_argnums`` is set, the default is based on calling
      ``inspect.signature(fun)`` to find corresponding named arguments.
    donate_argnums: Specify which arguments are "donated" to the computation.
      It is safe to donate arguments if you no longer need them once the
      computation has finished. In some cases XLA can make use of donated
      buffers to reduce the amount of memory needed to perform a computation,
      for example recycling one of your input buffers to store a result. You
      should not reuse buffers that you donate to a computation, JAX will raise
      an error if you try to.
    device: This is an experimental feature and the API is likely to change.
      Optional, the Device the jitted function will run on. (Available devices
      can be retrieved via :py:func:`jax.devices`.) The default is inherited
      from XLA's DeviceAssignment logic and is usually to use
      ``jax.devices()[0]``.
    backend: a string representing the XLA backend: ``'cpu'``, ``'gpu'``, or
      ``'tpu'``.

  Returns:
    A wrapped version of ``fn``, set up for just-in-time compilation.
  """
  if not isinstance(static_argnums, Iterable):
    static_argnums = (static_argnums,)
  if not isinstance(donate_argnums, Iterable):
    donate_argnums = (donate_argnums,)
  # offset argnums by two because first argument in the original function is the
  # scope while jitted has 3 functions before the user arguments.
  static_argnums = (0,) + tuple(i + 2 for i in static_argnums if i > 0)
  donate_argnums = tuple(i + 2 for i in donate_argnums if i > 0)

  # Close over scope_fn & repack_fn to avoid recompilation
  # this is impure but we use the fingerprint arg to differentiate between cases
  # where scope_fn or repack_fn actually produce non-identical results.
  jit_context = TransformContext[tuple[Callable, Callable]]()

  @functools.partial(
      jax.jit,
      static_argnums=static_argnums,
      static_argnames=static_argnames,
      donate_argnums=donate_argnums,
      device=device,
      backend=backend,
  )
  @functools.wraps(fn)
  def jitted(fingerprint, variable_groups, rng_groups, *args, **kwargs):
    scope_fn, repack_fn = jit_context.get()
    hash_key = fingerprint[1]
    # fingerprint is only used to differentiate the cache signature
    # del fingerprint
    scope = scope_fn(variable_groups, rng_groups)  # pylint: disable=not-callable
    y = fn(scope, hash_key, *args, **kwargs)
    return y, repack_fn(scope)  # pylint: disable=not-callable

  def inner(
      scope_fn,
      repack_fn,
      variable_groups,
      rng_groups,
      module_hash_key,
      *args,
      **kwargs,
  ):
    with jit_context.push((scope_fn, repack_fn)):
      scopes: list[Scope] = jax.tree_util.tree_leaves(
          scope_fn(variable_groups, rng_groups)
      )
      mutable = tuple(_hashable_filter(scope.mutable) for scope in scopes)

      rng_groups = jax.tree.map(
          lambda x: x.clear_suffix() if isinstance(x, LazyRng) else x,
          rng_groups,
          is_leaf=lambda x: isinstance(x, LazyRng),
      )

      fingerprint = (mutable, module_hash_key)
      capture_old_counts = jax.tree.map(
          lambda s: CountsHolder.make(s.rng_counters), scopes
      )
      res = jitted(fingerprint, variable_groups, rng_groups, *args, **kwargs)
      _restore_rng_counters(scopes, fingerprint, capture_old_counts)
      return res

  return pack(
      inner, (variables,), (variables,), (rngs,), name='jit', enable_kwargs=True
  )


def jit(
  target: Target,
  variables: CollectionFilter = True,
  rngs: PRNGSequenceFilter = True,
  static_argnums: int | Iterable[int] = (),
  static_argnames: str | Iterable[str] = (),
  donate_argnums: int | Iterable[int] = (),
  device=None,
  backend: str | None = None,
  methods=None,
) -> Target:
  """Lifted version of ``jax.jit``.

  Args:
    target: a ``Module`` or a function taking a ``Module`` as its first
      argument.
    variables: The variable collections that are lifted. By default all
      collections are lifted.
    rngs: The PRNG sequences that are lifted. By default all PRNG sequences are
      lifted.
    static_argnums: An int or collection of ints specifying which positional
      arguments to treat as static (compile-time constant). Operations that only
      depend on static arguments will be constant-folded in Python (during
      tracing), and so the corresponding argument values can be any Python
      object. Static arguments should be hashable, meaning both ``__hash__`` and
      ``__eq__`` are implemented, and immutable. Calling the jitted function
      with different values for these constants will trigger recompilation. If
      the jitted function is called with fewer positional arguments than
      indicated by ``static_argnums`` then an error is raised. Arguments that
      are not arrays or containers thereof must be marked as static. Defaults to
      ().
    static_argnames: An optional string or collection of strings specifying
      which named arguments to treat as static (compile-time constant). See the
      comment on ``static_argnums`` for details. If not provided but
      ``static_argnums`` is set, the default is based on calling
      ``inspect.signature(fun)`` to find corresponding named arguments.
    donate_argnums: Specify which arguments are "donated" to the computation. It
      is safe to donate arguments if you no longer need them once the
      computation has finished. In some cases XLA can make use of donated
      buffers to reduce the amount of memory needed to perform a computation,
      for example recycling one of your input buffers to store a result. You
      should not reuse buffers that you donate to a computation, JAX will raise
      an error if you try to.
    device: This is an experimental feature and the API is likely to change.
      Optional, the Device the jitted function will run on. (Available devices
      can be retrieved via :py:func:`jax.devices`.) The default is inherited
      from XLA's DeviceAssignment logic and is usually to use
      ``jax.devices()[0]``.
    backend: a string representing the XLA backend: ``'cpu'``, ``'gpu'``, or
      ``'tpu'``.
    methods: If ``target`` is a ``Module``, the methods of ``Module`` to jit.

  Returns:
    A wrapped version of target, set up for just-in-time compilation.
  """
  # TODO(marcvanzee): Improve docstrings (#1977).
  return lift_transform_cached(
      lift.jit,
      target,
      variables=variables,
      rngs=rngs,
      static_argnums=static_argnums,
      static_argnames=static_argnames,
      donate_argnums=donate_argnums,
      device=device,
      backend=backend,
      methods=methods,
  )


def jit(
  *,
  in_shardings: tp.Any = None,
  out_shardings: tp.Any = None,
  static_argnums: int | tp.Sequence[int] | None = None,
  static_argnames: str | tp.Iterable[str] | None = None,
  donate_argnums: int | tp.Sequence[int] | None = None,
  donate_argnames: str | tp.Iterable[str] | None = None,
  keep_unused: bool = False,
  device: tp.Optional[jax.Device] = None,
  backend: tp.Optional[str] = None,
  inline: bool = False,
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> tp.Callable[[tp.Callable[P, R]], JitWrapped[P, R]]: ...


def jit(
  fun: tp.Callable[P, R],
  *,
  in_shardings: tp.Any = None,
  out_shardings: tp.Any = None,
  static_argnums: int | tp.Sequence[int] | None = None,
  static_argnames: str | tp.Iterable[str] | None = None,
  donate_argnums: int | tp.Sequence[int] | None = None,
  donate_argnames: str | tp.Iterable[str] | None = None,
  keep_unused: bool = False,
  device: tp.Optional[jax.Device] = None,
  backend: tp.Optional[str] = None,
  inline: bool = False,
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> JitWrapped[P, R]: ...


def jit(
  fun: tp.Callable[P, R] | Missing = MISSING,
  *,
  in_shardings: tp.Any = None,
  out_shardings: tp.Any = None,
  static_argnums: int | tp.Sequence[int] | None = None,
  static_argnames: str | tp.Iterable[str] | None = None,
  donate_argnums: int | tp.Sequence[int] | None = None,
  donate_argnames: str | tp.Iterable[str] | None = None,
  keep_unused: bool = False,
  device: tp.Optional[jax.Device] = None,
  backend: tp.Optional[str] = None,
  inline: bool = False,
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> JitWrapped[P, R] | tp.Callable[[tp.Callable[P, R]], JitWrapped[P, R]]:
  """
  Lifted version of ``jax.jit`` that can handle Modules / graph nodes as
  arguments.

  .. note::
    If jitted function has a model and an optimizer as inputs, we can
    reduce accelerator's memory usage if we specify them in
    ``donate_argnums`` or ``donate_argnames``:

      >>> from flax import nnx
      >>>
      >>> @nnx.jit(donate_argnames=("model", "optimizer"))
      ... def func(model: nnx.Module, optimizer: nnx.Optimizer, other_args):
      ...   pass

    For details please see `this discussion <https://github.com/google/flax/issues/5026>`_.

  Args:
    fun: Function to be jitted. ``fun`` should be a pure function, as
      side-effects may only be executed once.

      The arguments and return value of ``fun`` should be arrays,
      scalars, or (nested) standard Python containers (tuple/list/dict) thereof.
      Positional arguments indicated by ``static_argnums`` can be anything at
      all, provided they are hashable and have an equality operation defined.
      Static arguments are included as part of a compilation cache key, which is
      why hash and equality operators must be defined.

      JAX keeps a weak reference to ``fun`` for use as a compilation cache key,
      so the object ``fun`` must be weakly-referenceable. Most :class:`Callable`
      objects will already satisfy this requirement.

      .. note::
        Bound methods (e.g., ``module.method``) are not supported. Use the
        decorator form ``@nnx.jit`` on the method definition or call
        ``nnx.jit(MyClass.method)(instance, ...)`` with the unbound method.
    in_shardings: Pytree of structure matching that of arguments to ``fun``,
      with all actual arguments replaced by resource assignment specifications.
      It is also valid to specify a pytree prefix (e.g. one value in place of a
      whole subtree), in which case the leaves get broadcast to all values in
      that subtree.

      The ``in_shardings`` argument is optional. JAX will infer the shardings
      from the input :py:class:`jax.Array`'s and defaults to replicating the input
      if the sharding cannot be inferred.

      The valid resource assignment specifications are:
        - :py:class:`Sharding`, which will decide how the value
            will be partitioned. With this, using a mesh context manager is not
            required.
        - :py:obj:`None`, will give JAX the freedom to choose whatever sharding
          it wants.
          For in_shardings, JAX will mark is as replicated but this behavior
          can change in the future.
          For out_shardings, we will rely on the XLA GSPMD partitioner to
          determine the output shardings.

      The size of every dimension has to be a multiple of the total number of
      resources assigned to it. This is similar to pjit's in_shardings.
    out_shardings: Like ``in_shardings``, but specifies resource
      assignment for function outputs. This is similar to pjit's
      out_shardings.

      The ``out_shardings`` argument is optional. If not specified, :py:func:`jax.jit`
      will use GSPMD's sharding propagation to figure out what the sharding of the
      output(s) should be.
    static_argnums: An optional int or collection of ints that specify which
      positional arguments to treat as static (compile-time constant).
      Operations that only depend on static arguments will be constant-folded in
      Python (during tracing), and so the corresponding argument values can be
      any Python object.

      Static arguments should be hashable, meaning both ``__hash__`` and
      ``__eq__`` are implemented, and immutable. Calling the jitted function
      with different values for these constants will trigger recompilation.
      Arguments that are not arrays or containers thereof must be marked as
      static.

      If neither ``static_argnums`` nor ``static_argnames`` is provided, no
      arguments are treated as static. If ``static_argnums`` is not provided but
      ``static_argnames`` is, or vice versa, JAX uses
      :code:`inspect.signature(fun)` to find any positional arguments that
      correspond to ``static_argnames``
      (or vice versa). If both ``static_argnums`` and ``static_argnames`` are
      provided, ``inspect.signature`` is not used, and only actual
      parameters listed in either ``static_argnums`` or ``static_argnames`` will
      be treated as static.
    static_argnames: An optional string or collection of strings specifying
      which named arguments to treat as static (compile-time constant). See the
      comment on ``static_argnums`` for details. If not
      provided but ``static_argnums`` is set, the default is based on calling
      ``inspect.signature(fun)`` to find corresponding named arguments.
    donate_argnums: Specify which positional argument buffers are "donated" to
      the computation. It is safe to donate argument buffers if you no longer
      need them once the computation has finished. In some cases XLA can make
      use of donated buffers to reduce the amount of memory needed to perform a
      computation, for example recycling one of your input buffers to store a
      result. You should not reuse buffers that you donate to a computation, JAX
      will raise an error if you try to. By default, no argument buffers are
      donated.

      If neither ``donate_argnums`` nor ``donate_argnames`` is provided, no
      arguments are donated. If ``donate_argnums`` is not provided but
      ``donate_argnames`` is, or vice versa, JAX uses
      :code:`inspect.signature(fun)` to find any positional arguments that
      correspond to ``donate_argnames``
      (or vice versa). If both ``donate_argnums`` and ``donate_argnames`` are
      provided, ``inspect.signature`` is not used, and only actual
      parameters listed in either ``donate_argnums`` or ``donate_argnames`` will
      be donated.

      For more details on buffer donation see the
      `FAQ <https://jax.readthedocs.io/en/latest/faq.html#buffer-donation>`_.
    donate_argnames: An optional string or collection of strings specifying
      which named arguments are donated to the computation. See the
      comment on ``donate_argnums`` for details. If not
      provided but ``donate_argnums`` is set, the default is based on calling
      ``inspect.signature(fun)`` to find corresponding named arguments.
    keep_unused: If `False` (the default), arguments that JAX determines to be
      unused by `fun` *may* be dropped from resulting compiled XLA executables.
      Such arguments will not be transferred to the device nor provided to the
      underlying executable. If `True`, unused arguments will not be pruned.
    device: This is an experimental feature and the API is likely to change.
      Optional, the Device the jitted function will run on. (Available devices
      can be retrieved via :py:func:`jax.devices`.) The default is inherited
      from XLA's DeviceAssignment logic and is usually to use
      ``jax.devices()[0]``.
    backend: This is an experimental feature and the API is likely to change.
      Optional, a string representing the XLA backend: ``'cpu'``, ``'gpu'``, or
      ``'tpu'``.
    inline: Specify whether this function should be inlined into enclosing
      jaxprs (rather than being represented as an application of the xla_call
      primitive with its own subjaxpr). Default False.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references, reference semantics, and
      structural changes to Modules inside the jitted function. If ``False``,
      uses tree-mode which treats Modules as regular JAX pytrees, avoiding
      the overhead of the graph protocol. Tree-mode is faster but does not
      support shared ``Variable`` references or returning mutable array
      references from the jitted function.

  Returns:
    A wrapped version of ``fun``, set up for just-in-time compilation.
  """

  if graph is None:
    graph = graphlib.set_graph_mode.current_value()
  if graph_updates is None:
    graph_updates = graphlib.set_graph_updates.current_value()
  if isinstance(fun, Missing):
    return functools.partial(
      jit,
      in_shardings=in_shardings,
      out_shardings=out_shardings,
      static_argnums=static_argnums,
      static_argnames=static_argnames,
      donate_argnums=donate_argnums,
      donate_argnames=donate_argnames,
      keep_unused=keep_unused,
      device=device,
      backend=backend,
      inline=inline,
      graph=graph,
      graph_updates=graph_updates,
    )  # type: ignore[return-value]
  fun_unbound, _, was_bound = _resolve_bound_callable(fun)
  if was_bound:
    _raise_bound_method_error('jit')

  if in_shardings is not None:
    extract.check_prefix(
      in_shardings, 'in_shardings', 'jit', graph, graph_updates
    )
  if out_shardings is not None:
    extract.check_prefix(
      out_shardings, 'out_shardings', 'jit', graph, graph_updates
    )

  wrapped_cls: tp.Any
  if graph and graph_updates:
    wrapped_cls = JitWrapped
  else:
    wrapped_cls = functools.partial(SimpleJitWrapped, graph=graph)
  return wrapped_cls(
    fun_unbound,
    in_shardings=in_shardings,
    out_shardings=out_shardings,
    static_argnums=static_argnums,
    static_argnames=static_argnames,
    donate_argnums=donate_argnums,
    donate_argnames=donate_argnames,
    keep_unused=keep_unused,
    device=device,
    backend=backend,
    inline=inline,
  )

