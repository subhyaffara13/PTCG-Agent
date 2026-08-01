
def jit_partial(
    fun: tp.Callable[..., R],
    *partial_args: tp.Any,
    in_shardings: tp.Any = None,
    out_shardings: tp.Any = None,
    donate_argnums: int | tp.Sequence[int] | None = None,
    donate_argnames: str | tp.Iterable[str] | None = None,
    keep_unused: bool = False,
    device: tp.Optional[jax.Device] = None,
    backend: tp.Optional[str] = None,
    inline: bool = False,
    graph: bool | None = None,
    graph_updates: bool | None = None,
) -> SimpleJitWrapped[..., R]:
  """JIT-compile ``fun`` with pre-flattened partial arguments.

  Similar to ``nnx.cached_partial`` but designed for tree-mode
  (``graph=False``). Each ``partial_arg`` is flattened into a
  ``PartialState`` whose pytree structure is fixed at construction time.
  Variable values inside partial arguments can still change between calls
  without triggering recompilation, and any mutations to Variables are
  propagated back to the originals after each call.

  Example usage::

    >>> from flax import nnx
    >>> import jax.numpy as jnp
    >>> import optax
    ...
    >>> x, y = jnp.ones((4, 2)), jnp.ones((4, 3))
    >>> model = nnx.Linear(2, 3, rngs=nnx.Rngs(0))
    >>> optimizer = nnx.Optimizer(model, optax.adamw(1e-3), wrt=nnx.Param)
    ...
    >>> def train_step(model, optimizer, x, y):
    ...   def loss_fn(model):
    ...     return jnp.mean((model(x) - y) ** 2)
    ...   loss, grads = nnx.value_and_grad(loss_fn)(model)
    ...   optimizer.update(model, grads)
    ...   return loss
    ...
    >>> train_step_fn = nnx.jit_partial(train_step, model, optimizer, graph=False)
    ...
    >>> loss = train_step_fn(x, y)

  Args:
    fun: The function to JIT-compile.
    *partial_args: Arguments to be pre-flattened and bound. These must
      appear as the first positional arguments of ``fun``.
    in_shardings: Sharding specification for inputs. When a tuple/list,
      the first ``len(partial_args)`` entries correspond to partial
      arguments and are broadcast against their original pytree
      structure. A non-tuple value (e.g. a single ``PartitionSpec``)
      is passed through directly to ``jax.jit`` and broadcast across
      all arguments uniformly.
    out_shardings: Like ``in_shardings``, but for function outputs.
    donate_argnums: Positional argument indices whose buffers may be
      donated to the computation.
    donate_argnames: Named arguments whose buffers may be donated.
    keep_unused: If ``True``, unused arguments are not pruned.
    device: Optional device to run on.
    backend: Optional backend to use.
    inline: If ``True``, inline the function.
    graph: If ``None``, uses the ``nnx_graph_mode`` config value.
    graph_updates: If ``True``, propagates updates on graph structure
      that happen inside the transform to the input graphs, has no
      effect when ``graph=False``. When ``False``, using
      ``StateSharding`` is not supported.

  Returns:
    A callable expecting the remaining (runtime)
    arguments.
  """
  if graph is None:
    graph = graphlib.set_graph_mode.current_value()
  if graph_updates is None:
    graph_updates = graphlib.set_graph_updates.current_value()
  if graph_updates and graph:
    raise ValueError(
      '`graph_updates` not supported by `jit_partial`'
    )
  if any(isinstance(x, StateSharding) for x in jax.tree.leaves(in_shardings)):
    raise ValueError(
      '`in_shardings` cannot contain `StateSharding` objects '
      'in `jit_partial`'
    )
  if any(isinstance(x, StateSharding) for x in jax.tree.leaves(out_shardings)):
    raise ValueError(
      '`out_shardings` cannot contain `StateSharding` objects '
      'in `jit_partial`'
    )

  is_variable = lambda x: isinstance(x, variablelib.Variable)
  ref_index = graphlib.RefMap() if graph else None
  flat_partial_args = tuple(
    _flatten_to_partial_state(arg, ref_index=ref_index)
    for arg in partial_args
  )

  jit_in_shardings: tp.Any = None
  if in_shardings is not None and isinstance(in_shardings, (tuple, list)) and not graph:
    num_partial = len(partial_args)
    partial_shardings = in_shardings[:num_partial]
    runtime_shardings = in_shardings[num_partial:]

    flat_partial_shardings = []
    for flat_arg, orig_arg, sharding in zip(
        flat_partial_args, partial_args, partial_shardings):
      broadcasted = extract.broadcast_prefix(
        sharding, orig_arg,
        prefix_is_leaf=lambda x: x is None
          or isinstance(x, variablelib.Variable),
        tree_is_leaf=is_variable,
      )
      flat_partial_shardings.append(
        PartialState(treedef=flat_arg.treedef, leaves=broadcasted)
      )
    jit_in_shardings = (*flat_partial_shardings, *runtime_shardings)
  else:
    jit_in_shardings = in_shardings

  @functools.wraps(fun)
  def wrapped_fun(*args, **kwargs):
    index_ref = graphlib.IndexMap() if graph else None
    def _unflatten(arg):
      if not isinstance(arg, PartialState):
        return arg
      elif graph:
        return graphlib.unflatten(
            arg.treedef, arg.leaves, index_ref=index_ref,
            copy_variables=False,
        )
      else:
        return jax.tree.unflatten(arg.treedef, arg.leaves)
    args = (_unflatten(a) for a in args)
    return fun(*args, **kwargs)

  return SimpleJitWrapped(
    wrapped_fun,
    in_shardings=jit_in_shardings,
    out_shardings=out_shardings,
    donate_argnums=donate_argnums,
    donate_argnames=donate_argnames,
    keep_unused=keep_unused,
    device=device,
    backend=backend,
    inline=inline,
    partial_args=flat_partial_args,
    graph=graph,
  )

