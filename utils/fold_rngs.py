
def fold_rngs(
    fn: Callable[..., Any],
    variables: CollectionFilter = True,
    rngs: PRNGSequenceFilter = True,
) -> Callable[..., Any]:
  # Close over scope_fn & repack_fn to avoid recompilation
  # this is impure but we use the fingerprint arg to differentiate between cases
  # where scope_fn or repack_fn actually produce non-identical results.
  fold_rngs_context = TransformContext[tuple[Callable, Callable]]()

  @functools.wraps(fn)
  def wrapped_fold_rngs(fingerprint, variable_groups, rng_groups, *args, **kwargs):
    scope_fn, repack_fn = fold_rngs_context.get()
    hash_key = fingerprint[1]
    # fingerprint is only used to differentiate the cache signature
    # del fingerprint
    scope = scope_fn(variable_groups, rng_groups)  # pylint: disable=not-callable
    y = fn(scope, hash_key, *args, **kwargs)
    return y, repack_fn(scope)  # pylint: disable=not-callable

  def inner_fold_rngs(
      scope_fn,
      repack_fn,
      variable_groups,
      rng_groups,
      module_hash_key,
      *args,
      **kwargs,
  ):
    with fold_rngs_context.push((scope_fn, repack_fn)):
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
      res = wrapped_fold_rngs(
          fingerprint, variable_groups, rng_groups, *args, **kwargs
      )
      _restore_rng_counters(scopes, fingerprint, capture_old_counts)
      return res

  return pack(
      inner_fold_rngs,
      (variables,),
      (variables,),
      (rngs,),
      name='fold_rngs',
      enable_kwargs=True,
  )


def fold_rngs(
    target: Target,
    variables: CollectionFilter = True,
    rngs: PRNGSequenceFilter = True,
) -> Target:
  return lift_transform_cached(
      lift.fold_rngs,
      target,
      variables=variables,
      rngs=rngs,
  )

