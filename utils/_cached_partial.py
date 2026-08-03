import functools

def _cached_partial(
    f: tp.Callable[..., tp.Any],
    *cached_args,
    graph: bool | None = None,
    graph_updates: bool | None = None,
):
  """Create a partial from a NNX transformed function alog with some cached input arguments
  and reduces the python overhead by caching the traversal of NNX graph nodes. This is useful
  for speed up function that are called repeatedly with the same subset of inputs e.g. a
  ``train_step`` with a ``model`` and ``optimizer``::

    >>> from flax import nnx
    >>> import jax.numpy as jnp
    >>> import optax
    ...
    >>> model = nnx.Linear(2, 3, rngs=nnx.Rngs(0))
    >>> optimizer = nnx.Optimizer(model, optax.adamw(1e-3), wrt=nnx.Param)
    ...
    >>> @nnx.jit
    ... def train_step(model, optimizer, x, y):
    ...   def loss_fn(model):
    ...     return jnp.mean((model(x) - y) ** 2)
    ...
    ...   loss, grads = nnx.value_and_grad(loss_fn)(model)
    ...   optimizer.update(model, grads)
    ...   return loss
    ...
    >>> cached_train_step = nnx.cached_partial(train_step, model, optimizer)
    ...
    >>> for step in range(total_steps:=2):
    ...   x, y = jnp.ones((10, 2)), jnp.ones((10, 3))
    ...   # loss = train_step(model, optimizer, x, y)
    ...   loss = cached_train_step(x, y)
    ...   print(f'Step {step}: loss={loss:.3f}')
    Step 0: loss=2.669
    Step 1: loss=2.660

  Note that ``cached_partial`` will clone all cached graph nodes to gurantee the validity
  of the cache, and these clones will contain references to the same Variable objects
  which guarantees that state is propagated correctly back to the original graph nodes.
  Because of the previous, the final structure of all graph nodes must be the same
  after each call to the cached function, otherwise an error will be raised. Temporary
  mutations are allowed (e.g. the use of ``Module.sow``) as long as they are cleaned up before
  the function returns (e.g. via ``nnx.pop``).

  Args:
    f: A function to cache.
    *cached_args: A subset of the input arguments containing the graph nodes to cache.

  Returns:
    A partial function expecting the remaining arguments to the original function.
  """
  if graph is None:
    graph = set_graph_mode.current_value()
  if graph_updates is None:
    graph_updates = set_graph_updates.current_value()

  if not graph or not graph_updates:
    raise ValueError(
      'cached_partial is a graph-mode-only API and requires graph_updates=True.'
    )
  cache: tp.MutableMapping[tp.Any, StaticCache] = PythonRefMap()  # type: ignore
  original_ref_index: RefMap = RefMap()
  index_ref: IndexMap = IndexMap()
  cached_ref_index: RefMap = RefMap()

  def create_static_cache(x):
    # TODO(cgarciae): support Array attribute updates for graph nodes
    if is_graph_node(x) or isinstance(x, Variable):
      graphdef, flat_state = flatten(
        x, with_paths=True, ref_index=original_ref_index, graph=True
      )
      paths = flat_state.paths
      variables = flat_state.leaves
      # clone but keep the same variable references
      node_cache = unflatten(
        graphdef, flat_state, index_ref=index_ref, copy_variables=False,
      )
      start_index = len(cached_ref_index)
      flatten(
        node_cache,
        ref_index=cached_ref_index,
        with_paths=False,
        graph=True,
      )
      cached_new_ref_index = RefMap(
        (key, value)
        for key, value in cached_ref_index.items()
        if value >= start_index
      )
      cache[node_cache] = StaticCache.create(
        graphdef, paths, variables, cached_new_ref_index
      )
      return node_cache
    return x

  cached_args = jax.tree.map(
    create_static_cache,
    cached_args,
    is_leaf=lambda x: is_graph_node(x) or isinstance(x, Variable),
  )

  @functools.wraps(f)
  def cache_args_wrapper(*args, **kwargs):
    with static_cache(cache):
      return f(*cached_args, *args, **kwargs)

  return cache_args_wrapper

