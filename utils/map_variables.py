
def map_variables(
  fn: Callable[..., Any],
  mapped_collections: CollectionFilter,
  map_in_fn: Callable[..., Any] = id_fn,
  map_out_fn: Callable[..., Any] = id_fn,
  init: bool = False,
  mutable: bool = False,
  rngs: PRNGSequenceFilter = True,
  variables: CollectionFilter = True,
) -> Callable[..., Any]:
  """Map Variables inside a scope.

  Args:
    fn: the function to be transformed.
    mapped_collections: the collection(s) to be transformed.
    map_in_fn: creates a view of the target variables.
    map_out_fn: transforms the updated variables in the view after mutation.
    init: If True, variables are initialized before transformation.
    mutable: If True, the mapped variable collections will be mutable.
    rngs: PRNGSequences added to the transformed scope (default: all).
    variables: Additional Variable collections added to the transformed scope.
      Besides those specified by `target` (default: all).

  Returns:
    A callable expecting a scope as the first argument.
  """
  is_target_out = mutable or init

  def wrapper(scope_fn, repack, variable_groups, rng_groups, *args, **kwargs):
    target, variables = variable_groups
    if init:
      scopes = scope_fn((target, variables), rng_groups)
      has_mutable_cols = any(
        not is_filter_empty(scope.mutable)
        for scope in jax.tree_util.tree_leaves(scopes)
      )
      if has_mutable_cols:
        fn(scopes, *args, **kwargs)
        target, _ = repack(scopes)
        target = tuple(map_out_fn(x) for x in target)
    target = tuple(map_in_fn(unfreeze(x)) for x in target)
    mfilter = True
    if not is_target_out:
      # mapped collections should not be mutable
      # unless the mapping supports it (by init=True or mutable=True)
      mfilter = subtract_filters(mfilter, mapped_collections)
    scopes = scope_fn((target, variables), rng_groups, mutable_filter=mfilter)
    y = fn(scopes, *args, **kwargs)
    out_target, out_vars = repack(scopes)
    if is_target_out:
      out_target = tuple(map_out_fn(x) for x in out_target)
    return y, (out_target, out_vars)

  in_vars = (mapped_collections, variables)
  out_vars = (
    in_vars
    if is_target_out
    else (False, subtract_filters(variables, mapped_collections))
  )
  return pack(
    wrapper,
    in_vars,
    out_vars,
    (rngs,),
    enable_kwargs=True,
    name='map_variables',
  )


def map_variables(
  target: Target,
  mapped_collections: CollectionFilter = True,
  trans_in_fn: Callable[..., Any] = lift.id_fn,
  trans_out_fn: Callable[..., Any] = lift.id_fn,
  init: bool = False,
  mutable: bool = False,
  rngs: PRNGSequenceFilter = True,
  variables: CollectionFilter = True,
  methods=None,
) -> Target:
  """Map Variables inside a module.

  ``map_variables`` can be used to transform the variables inside a module
  both before and after the module is applied. This is useful among other
  things for masking the weights of a module without having to modify the
  module itself.

  Example::

    >>> import jax
    >>> import jax.numpy as jnp
    >>> import flax.linen as nn
    ...
    >>> class CausalDense(nn.Module):
    ...   '''A dense layer that masks the weights such that the output is
    ...   causal, i.e. output i only depends on input <= i.
    ...   '''
    ...   features: int
    ...
    ...   def apply_mask(self, variables):
    ...     return (jax.tree_util.tree_map(jnp.triu, variables)
    ...             if not self.is_initializing() else variables)
    ...
    ...   def setup(self):
    ...     # temporary class
    ...     _CausalDense = nn.map_variables(
    ...       nn.Dense, 'params', self.apply_mask, init=self.is_initializing())
    ...     self.dense = _CausalDense(features=self.features, use_bias=False)
    ...
    ...   def __call__(self, x):
    ...     return self.dense(x)
    ...
    >>> module = CausalDense(features=5)
    >>> variables = module.init(jax.random.key(0), jnp.ones((1, 5)))

  Args:
    target: the module or function to be transformed.
    mapped_collections: the collection(s) to be transformed.
    trans_in_fn: modifies the variables before applying the module or function.
    trans_out_fn: modifies the variables after applying the module or function,
      it is only applied if either ``init`` or ``mutable`` are not False.
    init: If True, variables are initialized before transformation.
    mutable: If True, the mapped variable collections will be mutable.
    rngs: PRNGSequences added to the transformed scope (default: all).
    variables: Additional Variable collections added to the transformed scope.
      Besides those specified by ``target`` (default: all).
    methods: If ``target`` is a ``Module``, the methods of ``Module`` to map
      variables for.

  Returns:
    a wrapped version of ``target`` that will map the specified collections.
  """

  return lift_transform(
    lift.map_variables,
    target,
    mapped_collections,
    trans_in_fn,
    trans_out_fn,
    init,
    mutable,
    rngs,
    variables,
    methods=methods,
  )

