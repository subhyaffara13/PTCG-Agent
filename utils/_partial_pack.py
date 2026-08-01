
def _partial_pack(
    scope_tree: Scope,
    in_variable_filters: Sequence[CollectionFilter],
    out_variable_filters: Sequence[CollectionFilter],
    rng_filters: Sequence[PRNGSequenceFilter],
    name=None,
) -> tuple[Callable[..., Any], Callable[..., Any], Any, Any, Callable[..., Any]]:
  """Pack variables and rngs for functional transformations.

  The _partial_pack function is the building block for all other lifted transformations.

  Args:
    fn: The function to pack. `fn` has the signature
    in_variable_filters: Input variable filters.
    out_variable_filters: Output variable filters.
    rng_filters: RNG filters.
    name: The name of the packed scope.
    enable_kwargs: Whether to enable kwargs or not.
  Returns:
    `(scope_fn, repack_fn, variable_groups, rng_groups, publish_results_fn)`
  """
  # pylint: disable=protected-access
  scopes, treedef = jax.tree_util.tree_flatten(scope_tree)
  scopes, paths = _dedup_scopes(scopes)

  variable_groups_xs = []

  for scope in scopes:
    scope._validate_trace_level()
    scope._populate_collections()
    variable_groups_xs.append(
        group_collections(scope._variables, in_variable_filters)
    )
  variable_groups_xs_t = _transpose(variable_groups_xs)

  # Make sure that in-only variable collections are frozen
  for variable_group_xs in variable_groups_xs_t:
    for variable_group in variable_group_xs:
      for col_name, collection in variable_group.items():
        col_in_out = any(
            in_filter(col_filter, col_name)
            for col_filter in out_variable_filters
        )
        if not col_in_out:
          variable_group[col_name] = freeze(collection)
  rng_groups_xs = []
  inner_rng_counters = []
  for scope in scopes:
    rng_counters = scope.rng_counters
    rng_groups = group_collections(scope.rngs, rng_filters)
    rng_groups_xs.append(rng_groups)
    inner_rng_counters.append(rng_counters)
  rng_groups_xs_t = _transpose(rng_groups_xs)

  def scope_fn(
      variable_groups_xs_t,
      rng_groups_xs_t,
      mutable_filter: CollectionFilter = True,
  ):
    inner_scopes = []
    mutable: Filter = False
    for out_filter in out_variable_filters:
      mutable = union_filters(mutable, out_filter)
    # could be () in the edge case where no rngs or variable_groups are lifted
    # in this case fallback to ((),) * len(scopes) to make sure the zip has
    # something to iterate over for each scope.
    variable_groups_xs = _transpose(variable_groups_xs_t) or ((),) * len(
        scopes
    )
    rng_groups_xs = _transpose(rng_groups_xs_t) or ((),) * len(scopes)
    assert len(variable_groups_xs) == len(scopes)
    assert len(rng_groups_xs) == len(scopes)
    for variable_groups, rng_groups, scope, rng_counters in zip(
        variable_groups_xs, rng_groups_xs, scopes, inner_rng_counters
    ):
      variables = {}
      rngs = {}
      for variable_group in variable_groups:
        variables.update(variable_group)
      for rng_group in rng_groups:
        rngs.update(rng_group)
      # make sure variable dicts are cloned and can't be manipulated by ref
      # sharing.
      variables = jax.tree_util.tree_map(lambda x: x, variables)
      scope_mutable = intersect_filters(
          intersect_filters(scope.mutable, mutable), mutable_filter
      )
      new_debug_path = scope.debug_path
      if name:
        if new_debug_path:
          new_debug_path = new_debug_path[:-1] + (
              f'{name}({new_debug_path[-1]})',
          )
        else:
          new_debug_path = (f'{name}()',)
      inner_scope = Scope(
          variables,
          name=scope.name,
          rngs=rngs,
          mutable=scope_mutable,
          parent=None,
          path=scope.path,
          debug_path=new_debug_path,
          flags=scope.flags,
      )
      inner_scope.rng_counters = rng_counters
      inner_scopes.append(inner_scope)
    inner_scopes = _dup_scopes(scopes, inner_scopes, paths)
    return treedef.unflatten(inner_scopes)

  def repack_fn(inner_scope_tree):
    inner_scopes = treedef.flatten_up_to(inner_scope_tree)
    inner_scopes, inner_paths = _dedup_scopes(inner_scopes)
    inner_scopes = list(inner_scopes)
    assert [p for _, p in paths] == [p for _, p in inner_paths]
    out_variable_groups_xs = []
    for inner_scope in inner_scopes:
      inner_scope.invalidate()
      inner_scope._validate_trace_level()
      mutable_variables = {
          key: val
          for key, val in inner_scope._variables.items()
          if in_filter(inner_scope.mutable, key)
      }
      out_variable_groups = group_collections(
          mutable_variables, tuple(out_variable_filters) + (True,)
      )
      remainder = tuple(out_variable_groups[-1].keys())
      if remainder:
        raise ValueError(f'unmapped output variables: {remainder}')
      out_variable_groups_xs.append(out_variable_groups[:-1])

    return _transpose(out_variable_groups_xs)

  def publish_results_fn(out_variable_groups_xs_t):
    out_variable_groups_xs = _transpose(out_variable_groups_xs_t)
    for scope, out_variable_groups, rng_counters in zip(
        scopes, out_variable_groups_xs, inner_rng_counters
    ):
      for out_variable_group in out_variable_groups:
        for col_name, collection in out_variable_group.items():
          if not scope.is_mutable_collection(col_name):
            # Some lifted transforms like scan return redundant variables.
            continue
          for var_name, value in collection.items():
            scope.put_variable(col_name, var_name, value)

  return (
      scope_fn,
      repack_fn,
      variable_groups_xs_t,
      rng_groups_xs_t,
      publish_results_fn,
    )

