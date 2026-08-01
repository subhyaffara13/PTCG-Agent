
def switch(
    key: Callable[[_S], _T],
    ruledict: Mapping[_T, Callable[[_S], _S]]
) -> Callable[[_S], _S]:
    """ Select a rule based on the result of key called on the function """
    def switch_rl(expr: _S) -> _S:
        rl = ruledict.get(key(expr), identity)
        return rl(expr)
    return switch_rl


def switch(flag: _ods_ir.Value[_ods_ir.IntegerType], default_operands: _Sequence[_ods_ir.Value], case_operands: _Sequence[_ods_ir.Value], case_operand_segments: _Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr], default_destination: _ods_ir.Block, case_destinations: _Sequence[_ods_ir.Block], *, case_values: _Optional[_Union[_Any, _ods_ir.DenseIntElementsAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> SwitchOp:
  return SwitchOp(flag=flag, defaultOperands=default_operands, caseOperands=case_operands, case_operand_segments=case_operand_segments, defaultDestination=default_destination, caseDestinations=case_destinations, case_values=case_values, loc=loc, ip=ip)


def switch(value: _ods_ir.Value[_ods_ir.IntegerType], default_operands: _Sequence[_ods_ir.Value], case_operands: _Sequence[_ods_ir.Value], case_operand_segments: _Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr], default_destination: _ods_ir.Block, case_destinations: _Sequence[_ods_ir.Block], *, case_values: _Optional[_Union[_Any, _ods_ir.DenseIntElementsAttr]] = None, branch_weights: _Optional[_Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> SwitchOp:
  return SwitchOp(value=value, defaultOperands=default_operands, caseOperands=case_operands, case_operand_segments=case_operand_segments, defaultDestination=default_destination, caseDestinations=case_destinations, case_values=case_values, branch_weights=branch_weights, loc=loc, ip=ip)


def switch(index, branches: Sequence[Callable], *operands: Any,
           operand: Any = _no_operand_sentinel):
  """Apply exactly one of the ``branches`` given by ``index``.

  If ``index`` is out of bounds, it is clamped to within bounds.

  Has the semantics of the following Python::

    def switch(index, branches, *operands):
      index = clamp(0, index, len(branches) - 1)
      return branches[index](*operands)

  Internally this wraps XLA's `Conditional
  <https://www.openxla.org/xla/operation_semantics#conditional>`_
  operator. However, when transformed with :func:`~jax.vmap` to operate over a
  batch of predicates, ``cond`` is converted to :func:`~jax.lax.select`.

  Args:
    index: Integer scalar type, indicating which branch function to apply.
    branches: Sequence of functions (A -> B) to be applied based on ``index``.
      All branches must return the same output structure.
    operands: Operands (A) input to whichever branch is applied.

  Returns:
    Value (B) of ``branch(*operands)`` for the branch that was selected based
    on ``index``.
  """
  if not all(callable(branch) for branch in branches):
    raise TypeError("lax.switch: branches argument should be a sequence of callables.")
  if operand is not _no_operand_sentinel:
    if operands:
      raise TypeError("if 'operand' keyword is passed then no positional "
                      f"operands can be passed, got {operand=} "
                      f"and positional operands {operands}")
    operands = (operand,)
  del operand

  if len(np.shape(index)) != 0:
    raise TypeError(
        f"Branch index must be scalar, "
        f"got {index} of shape {np.shape(index)}.")

  try:
    index_dtype = dtypes.result_type(index)
  except TypeError as err:
    msg = f"Index type must be an integer, got {index}."
    raise TypeError(msg) from err

  if index_dtype.kind not in 'iu':
    raise TypeError(
        f"Index type must be an integer, got {index} as {index_dtype}")

  branches = tuple(branches)

  if len(branches) == 0:
    raise ValueError("Empty branch sequence")
  elif len(branches) == 1:
    return branches[0](*operands)

  index = lax.convert_element_type(index, np.int32)
  lo = np.array(0, np.int32)
  hi = np.array(len(branches) - 1, np.int32)
  index = lax.clamp(lo, index, hi)
  return _switch_internal(index, branches, operands,
                          branches_platforms=None)


def switch(
  index: Any,
  branches: Sequence[Callable[..., C]],
  scope: Scope,
  *operands,
  variables: CollectionFilter = True,
  rngs: PRNGSequenceFilter = True,
) -> C:
  """Lifted version of ``jax.lax.switch``.

  The returned values from ``branches``
  must have the same Pytree structure, shapes, and dtypes.
  The variables created or updated inside the
  branches must also have the same structure.
  Note that this constraint is violated when
  creating variables or submodules in only one branch.
  Because initializing variables in just one branch
  causes the parameter structure to be different.

  Example::

    def switch_example(scope, x, index):
      scope.variable('state', 'a_count', lambda: 0)
      scope.variable('state', 'b_count', lambda: 0)
      scope.variable('state', 'c_count', lambda: 0)
      def a_fn(scope, x):
        scope.variable('state', 'a_count').value += 1
        return scope.child(nn.dense)(x, 2)
      def b_fn(scope, x):
        scope.variable('state', 'b_count').value += 1
        return -scope.child(nn.dense)(x, 2)
      def c_fn(scope, x):
        scope.variable('state', 'c_count').value += 1
        return scope.child(nn.dense)(x, 2)
      return lift.switch(index, [a_fn, b_fn, c_fn], scope, x)

  If you want to have a different parameter structure for each branch
  you should run all branch on initialization before calling switch::

    def multihead_switch_example(scope, x, index):
      def a_fn(scope, x):
        x = scope.child(nn.dense)(x, 10)
        x = scope.child(nn.dense)(x, 7)
        return scope.child(nn.dense)(x, 5)
      def b_fn(scope, x):
        x = scope.child(nn.dense)(x, 11)
        return scope.child(nn.dense)(x, 5)
      def c_fn(scope, x):
        return scope.child(nn.dense)(x, 5)

      branches = [a_fn, b_fn, c_fn]

      # run all branches on init
      if scope.is_mutable_collection('params'):
        for branch in branches:
          _ = branch(scope, x)

      return lift.switch(index, branches, scope, x)

  Args:
    index: Integer scalar type, indicating which branch function to apply.
    branches: Sequence of functions to be applied based on index.
      The signature of each function is (Scope, *operands) -> T.
    scope: A Scope or Pytree of scopes to pass
    *operands: The arguments passed to ``true_fun`` and ``false_fun``
    variables: The variable collections passed to the conditional
      branches (default: all)
    rngs: The PRNG sequences passed to the conditionals (default: all)
  Returns:
    The result of the evaluated branch.
  """

  def inner(scope_fn, repack_fn, variable_groups, rng_groups):
    def branch_wrapper(branch_fn, *operands):
      scope = scope_fn(variable_groups, rng_groups)
      y = branch_fn(scope, *operands)
      return y, repack_fn(scope)

    pure_branches = [
      functools.partial(branch_wrapper, branch_fn) for branch_fn in branches
    ]
    return jax.lax.switch(index, pure_branches, *operands)

  return pack(inner, (variables,), (variables,), (rngs,), name='switch')(scope)


def switch(
  index: Any,
  branches: Sequence[Callable[..., C]],
  mdl: Module,
  *operands,
  variables: CollectionFilter = True,
  rngs: PRNGSequenceFilter = True,
) -> C:
  """Lifted version of ``jax.lax.switch``.

  The returned values from ``branches``
  must have the same Pytree structure, shapes, and dtypes.
  The variables created or updated inside the
  branches must also have the same structure.
  Note that this constraint is violated when
  creating variables or submodules in only one branch.
  Because initializing variables in just one branch
  causes the parameter structure to be different.

  Example::

    >>> import flax.linen as nn

    >>> class SwitchExample(nn.Module):
    ...   @nn.compact
    ...   def __call__(self, x, index):
    ...     self.variable('state', 'a_count', lambda: 0)
    ...     self.variable('state', 'b_count', lambda: 0)
    ...     self.variable('state', 'c_count', lambda: 0)
    ...     def a_fn(mdl, x):
    ...       mdl.variable('state', 'a_count').value += 1
    ...       return nn.Dense(2, name='dense')(x)
    ...     def b_fn(mdl, x):
    ...       mdl.variable('state', 'b_count').value += 1
    ...       return -nn.Dense(2, name='dense')(x)
    ...     def c_fn(mdl, x):
    ...       mdl.variable('state', 'c_count').value += 1
    ...       return nn.Dense(2, name='dense')(x)
    ...     return nn.switch(index, [a_fn, b_fn, c_fn], self, x)

  If you want to have a different parameter structure for each branch
  you should run all branches on initialization before calling switch::

    >>> class MultiHeadSwitchExample(nn.Module):
    ...   def setup(self) -> None:
    ...     self.heads = [
    ...       nn.Sequential([nn.Dense(10), nn.Dense(7), nn.Dense(5)]),
    ...       nn.Sequential([nn.Dense(11), nn.Dense(5)]),
    ...       nn.Dense(5),
    ...     ]
    ...
    ...   @nn.compact
    ...   def __call__(self, x, index):
    ...     def head_fn(i):
    ...       return lambda mdl, x: mdl.heads[i](x)
    ...     branches = [head_fn(i) for i in range(len(self.heads))]
    ...
    ...     # run all branches on init
    ...     if self.is_mutable_collection('params'):
    ...       for branch in branches:
    ...         _ = branch(self, x)
    ...
    ...     return nn.switch(index, branches, self, x)

  Args:
    index: Integer scalar type, indicating which branch function to apply.
    branches: Sequence of functions to be applied based on index.
      The signature of each function is (module, *operands) -> T.
    mdl: A Module target to pass.
    *operands: The arguments passed to the branches.
    variables: The variable collections passed to the conditional
      branches (default: all)
    rngs: The PRNG sequences passed to the conditionals (default: all)
  Returns:
    The result of the evaluated branch.
  """
  return lift_direct_transform(
    _switch_wrapper,
    tuple(branches),
    mdl,
    index,
    *operands,
    variables=variables,
    rngs=rngs,
    n_branches=len(branches),
  )


def switch(
  index,
  branches: tp.Sequence[tp.Callable[..., A]],
  *operands,
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> A:
  """Select and apply one of ``branches`` based on ``index``.

  Wraps `jax.lax.switch <https://jax.readthedocs.io/en/latest/_autosummary/jax.lax.switch.html>`__
  to support Flax NNX modules and variables.

  Args:
    index: integer scalar indicating which branch to apply.
    branches: sequence of functions to select from.
    *operands: operands passed to the selected branch.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references and reference semantics.
      If ``False``, uses tree-mode which treats Modules as regular JAX
      pytrees, avoiding the overhead of the graph protocol.
    graph_updates: If ``True``, propagates updates on graph structure
      that happen inside the transform to the input graphs, has no
      effect when ``graph=False``.
  """
  if graph is None:
    graph = graphlib.set_graph_mode.current_value()
  if graph_updates is None:
    graph_updates = graphlib.set_graph_updates.current_value()
  if not graph or not graph_updates:
    if graph:
      operands = extract.to_tree2(operands)
    extract.check_no_aliases('switch', operands=operands)
    out, updates = jax.lax.switch(
      index,
      [SimpleCondFn(f, graph=graph) for f in branches],
      *operands,
    )
    if graph:
      out = extract.from_tree2(out)
    extract.apply_variable_updates(operands, updates)
    return out

  @general.split_inputs(ctxtag='switch')
  def _switch(index, branches, *operands):
    return jax.lax.switch(
      index,
      [general.merge_inputs(f, ctxtag='switch') for f in branches],
      *operands,
    )

  return _switch(index, branches, *operands)

