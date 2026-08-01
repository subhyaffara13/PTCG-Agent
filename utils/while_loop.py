
def while_loop(cond_fn, body_fn, carried_inputs):
    r"""
    Run ``body_fn(*carried_inputs)`` while ``cond_fn(*carried_inputs)`` returns
    a True scalar tensor. Returns the output of body_fn or initial
    carried_inputs.

    .. warning::

        `torch.while_loop` is a prototype feature in PyTorch. It has limited support for input and output types and
        doesn't support training currently. Please look forward to a more stable implementation in a future version of PyTorch.
        Read more about feature classification at: https://pytorch.org/blog/pytorch-feature-classification-changes/#prototype

    `while_loop` is a structured control flow operator. It preserves the loop semantic across the torch.compile and torch.export.

    `while_loop` is equivalent to the following::

        def while_loop(cond_fn, body_fn, carried_inputs):
            val = carried_inputs
            while cond_fn(*val):
                val = body_fn(*val)
            return val

    Args:
        cond_fn (Callable): A callable function that returns a boolean Scalar tensor or a python boolean.

        body_fn (Callable): A callable function that takes the same inputs as `cond_fn` and returns a tuple of tensors or ints

        carried_inputs (Tuple of possibly nested dict/list/tuple of tensors or ints): A tuple of inputs to cond_fn and body_fn.
            It's also the initial value of states that are carried across iterations. Note that when pass an integer as carry,
            the corresponding return of while_loop will be another int with unknown values because we don't know how many
            iterations while_loop will run.

    Example 1::

        def cond_fn(iter, x):
            return iter.sum() < 10


        def body_fn(iter, x):
            return iter + 1, x.sin()


        while_loop(cond_fn, body_fn, (torch.zeros(1), torch.randn(3, 4)))

    Example 2::

        def cond_fn(int_iter, x):
            return 2 * int_iter < x.shape[0]


        def body_fn(int_iter, x):
            return int_iter + 1, x + int_iter


        while_loop(cond_fn, body_fn, (0, torch.randn(3, 4)))

    Restrictions:

        - body_fn must return tensors or int with the same metadata (e.g.shape, dtype) as inputs.

        - body_fn and cond_fn must not in-place mutate the carried_inputs. A clone before the mutation is required.

        - body_fn and cond_fn must not mutate python variables (e.g. list/dict) created outside of the body_fn.

        - body_fn and cond_fn's output cannot alias any of the inputs. A clone is required.

    .. warning::

        Temporal Limitations:

        - 'while_loop' only supports **inference** right now. Autograd will be supported in the future.

    """

    # Currently, additional_inputs is not a user-facing input. It will be automatically set in dynamo.
    # parameters and buffers accessed in cond_fn or body_fn or tensor closures will become additional_inputs.
    additional_inputs: tuple = ()

    # The reason we flatten the output before calling into dynamo is that
    # we want to create a consistent input ordering for cond_fn and body_fn.
    # and we also want to the input ordering matches the output ordering.
    # Also see NOTE: [why we cannot use "automatic" for while_loop]
    # Construct flat cond_fn and flat_body_fn, which takes flattened inputs
    flat_inputs, in_spec = pytree.tree_flatten((carried_inputs, additional_inputs))

    def flat_cond_fn(*flat_args):
        carried, additional = pytree.tree_unflatten(flat_args, in_spec)
        return cond_fn(*carried, *additional)

    def flat_body_fn(*flat_args):
        carried, additional = pytree.tree_unflatten(flat_args, in_spec)
        return body_fn(*carried, *additional)

    if torch.compiler.is_dynamo_compiling():
        return while_loop_op(flat_cond_fn, flat_body_fn, tuple(flat_inputs), tuple())

    def _validate_input(cond_fn, body_fn, carried_inputs):
        from torch._higher_order_ops.utils import validate_subgraph_args_types

        if not callable(cond_fn) or not callable(body_fn):
            raise RuntimeError("Expect cond_fn and body_fn to be callable.")

        validate_subgraph_args_types(flat_inputs)

        if not pytree.tree_all(
            lambda t: isinstance(t, (torch.Tensor, torch.SymInt, int)), carried_inputs
        ):
            raise RuntimeError(
                "Expect carried_inputs to be a tuple of possibly nested dict/list/tuple that only"
                f"consists of tensor or int leaves, but got {carried_inputs}."
            )

    _validate_input(cond_fn, body_fn, carried_inputs)

    # Dynamo is expecting a callable with "__code__" attribute.
    # We cannot directly pass cond_op to it. So we wrap it in a dummy function.
    def _while_loop_op_wrapper(*args, **kwargs):
        return while_loop_op(*args, **kwargs)

    from torch._higher_order_ops.utils import _hop_compile_and_call

    return _hop_compile_and_call(
        _while_loop_op_wrapper,
        (flat_cond_fn, flat_body_fn, tuple(flat_inputs), tuple()),
    )


def while_loop(cond_fn, body_fn, carried_inputs, additional_inputs, stack_output=False):
    # TODO: when graph_partition is enabled, skip - partitioning handles control flow
    # we run into memory cleanup issue
    if not config.graph_partition and any(
        isinstance(x, IRNode) and is_triton(x)
        for x in carried_inputs + additional_inputs
    ):
        msg = "control flow operator: torch.while_loop."
        if stack_trace := V.graph.current_node.meta.get("stack_trace", None):
            msg = f"{msg} Found from : \n {stack_trace}"
        V.graph.disable_cudagraphs_reason = msg

    result = ir.WhileLoop.create(
        cond_fn, body_fn, carried_inputs, additional_inputs, stack_output
    )
    assert isinstance(result, Sequence)
    return list(map(ir.WhileLoop._maybe_wrap_as_tensor_box, result))


def while_loop(cond_fun: Callable[[T], BooleanNumeric],
               body_fun: Callable[[T], T],
               init_val: T) -> T:
  """Call ``body_fun`` repeatedly in a loop while ``cond_fun`` is True.

  The `Haskell-like type signature`_ in brief is

  .. code-block:: haskell

    while_loop :: (a -> Bool) -> (a -> a) -> a -> a

  The semantics of ``while_loop`` are given by this Python implementation::

    def while_loop(cond_fun, body_fun, init_val):
      val = init_val
      while cond_fun(val):
        val = body_fun(val)
      return val

  Unlike that Python version, ``while_loop`` is a JAX primitive and is lowered
  to a single WhileOp. That makes it useful for reducing compilation times
  for jit-compiled functions, since native Python loop constructs in an ``@jit``
  function are unrolled, leading to large XLA computations.

  Also unlike the Python analogue, the loop-carried value ``val`` must hold a
  fixed shape and dtype across all iterations (and not just be consistent up to
  NumPy rank/shape broadcasting and dtype promotion rules, for example). In
  other words, the type ``a`` in the type signature above represents an array
  with a fixed shape and dtype (or a nested tuple/list/dict container data
  structure with a fixed structure and arrays with fixed shape and dtype at the
  leaves).

  Another difference from using Python-native loop constructs is that
  ``while_loop`` is not reverse-mode differentiable because XLA computations
  require static bounds on memory requirements.

  .. note::
    :py:func:`while_loop` compiles ``cond_fun`` and ``body_fun``, so while it
    can be combined with :py:func:`jit`, it's usually unnecessary.

  Args:
    cond_fun: function of type ``a -> Bool``.
    body_fun: function of type ``a -> a``.
    init_val: value of type ``a``, a type that can be a scalar, array, or any
      pytree (nested Python tuple/list/dict) thereof, representing the initial
      loop carry value.

  Returns:
    The output from the final iteration of body_fun, of type ``a``.

  .. _Haskell-like type signature: https://wiki.haskell.org/Type_signature
  """
  if not (callable(body_fun) and callable(cond_fun)):
    raise TypeError("lax.while_loop: body_fun and cond_fun arguments should be callable.")
  if config.disable_jit.value:
    try:
      val = tree_map(lax.asarray, init_val)
      while cond_fun(val):
        val = tree_map(lax.asarray, body_fun(val))
      return val
    except core.ConcretizationTypeError:
      # Can't run this while_loop in Python (e.g. because there's a vmap
      # transformation on it), so we fall back to the primitive version.
      pass

  def _create_jaxpr(init_avals):
    args_avals = FlatTree.pack(((init_avals,), {}))
    cond_jaxpr, cond_out_avals = pe.trace_to_jaxpr(cond_fun, args_avals, cond_dbg)
    body_jaxpr, body_out_avals = pe.trace_to_jaxpr(body_fun, args_avals, body_dbg)
    if not treedef_is_leaf(cond_out_avals.tree) or len(cond_jaxpr.out_avals) != 1:
      msg = "cond_fun must return a boolean scalar, but got pytree {}."
      raise TypeError(msg.format(cond_out_avals.tree))

    pred_aval = cond_jaxpr.out_avals[0]
    if (not isinstance(pred_aval, ShapedArray)
        or ShapedArray(pred_aval.shape, pred_aval.dtype) != ShapedArray((), np.bool_)):
      msg = "cond_fun must return a boolean scalar, but got output type(s) {}."
      raise TypeError(msg.format(cond_jaxpr.out_avals))

    return cond_jaxpr, body_jaxpr, body_out_avals

  cond_dbg = api_util.debug_info("while_cond", cond_fun, (init_val,), {})
  body_dbg = api_util.debug_info("while_body", body_fun, (init_val,), {})
  init_val_flat = FlatTree.flatten(init_val)
  check_no_transformed_refs_args(lambda: body_dbg, init_val_flat.vals)
  del init_val
  init_aval = init_val_flat.map(core.typeof)

  # The body input and output avals must match exactly. However, we want to account for
  # the case when init contains weakly-typed values (e.g. Python scalars), with avals that
  # may not match the output despite being compatible by virtue of their weak type.
  # To do this, we compute the jaxpr in two passes: first with the raw inputs, and if
  # necessary, a second time with modified init values.
  cond_jaxpr, body_jaxpr, body_out_avals = _create_jaxpr(init_aval)
  if len(body_out_avals) != len(init_aval):
    _check_carry_type('while_loop body', body_fun, init_aval, body_out_avals)
    assert False, "shouldn't get here"

  init_val_flat, changed = init_val_flat.map3(
      _promote_weak_typed_input,
      list(init_aval), body_out_avals).unzip2()
  if any(changed):
    init_aval = init_val_flat.map(core.typeof)
    cond_jaxpr, body_jaxpr, body_out_avals = _create_jaxpr(init_aval)

  cond_jaxpr, cond_consts = pe.separate_consts(cond_jaxpr)
  body_jaxpr, body_consts = pe.separate_consts(body_jaxpr)
  _check_carry_type('while_loop body', body_fun, init_aval, body_out_avals)

  if not all(not v.aval.has_qdd or v.initial_qdd == v.final_qdd for v in
             body_jaxpr.jaxpr.invars):
    raise TypeError("type-changing mutations not allowed in while_loop body")
  joined_effects = core.join_effects(cond_jaxpr.effects, body_jaxpr.effects)
  disallowed_effects = effects.control_flow_allowed_effects.filter_not_in(joined_effects)
  if disallowed_effects:
    raise NotImplementedError(
        f'Effects not supported in `while`: {disallowed_effects}')

  # If the body forwards an input carry to an output carry, *and* it's not used
  # by the cond fun, it can be moved to be a body const. Doing so can lead to
  # efficiency wins: if e.g. we vmap the loop with a batched predicate, we batch
  # the carry too, but not the body consts.
  body_fwd = pe._jaxpr_forwarding(body_jaxpr.jaxpr)
  carry_nofwd = [len(body_consts) + i != f for i, f in enumerate(body_fwd)]
  cond_jaxpr_, keep_cond = pe.dce_jaxpr(
      cond_jaxpr.jaxpr, [True], [True] * len(cond_consts) + carry_nofwd)
  _, keep_cond_carry = split_list(keep_cond, [len(cond_consts)])
  move_to_const = _map(operator.not_, keep_cond_carry)

  init_vals = list(init_val_flat)
  new_body_consts: list[Any] = []
  if any(move_to_const):
    cond_jaxpr = pe.close_jaxpr(cond_jaxpr_)
    body_jaxpr = pe.prune_closed_jaxpr_outputs(
        body_jaxpr, [not m for m in move_to_const])
    body_jaxpr = pe.move_binders_to_front(
        body_jaxpr, [False] * len(body_consts) + move_to_const)
    init_vals, new_body_consts = partition_list(move_to_const, init_vals)
    body_consts = [*new_body_consts, *body_consts]

  outs = while_p.bind(*cond_consts, *body_consts, *init_vals,
                      cond_nconsts=len(cond_consts), cond_jaxpr=cond_jaxpr,
                      body_nconsts=len(body_consts), body_jaxpr=body_jaxpr)

  if any(move_to_const):
    outs = pe.merge_lists(move_to_const, outs, new_body_consts)

  return body_out_avals.update(outs).unflatten()


def while_loop(
  cond_fn: Callable[[Scope, C], bool],
  body_fn: Callable[[Scope, C], C],
  scope: Scope,
  init: C,
  carry_variables: CollectionFilter = False,
  broadcast_variables: CollectionFilter = True,
  split_rngs: Mapping[PRNGSequenceFilter, bool] = {},
) -> C:
  """Lifted version of jax.lax.while_loop.

  The lifted scope is passed to `cond_fn` and `body_fn`.
  Broadcasted variables are immutable. The carry variable are
  mutable but cannot change shape and dtype.
  This also means you cannot initialize variables inside
  the body. Consider calling `body_fn` once manually before
  calling `while_loop` if variable initialization is required.

  Example::

    def f(scope, x):
      def cond_fn(scope, c):
        return scope.get_variable('state', 'acc') < 10
      def body_fn(scope, c):
        acc = scope.variable('state', 'acc')
        acc += 1
        y = scope.child(nn.dense)(c, c.shape[-1])
        return y

      c = x
      c = body_fn(scope, c)
      return lift.while_loop(cond_fn, body_fn, scope, (),
                             carry_variables='state')

  Args:
    cond_fn: Should return True as long as the loop should continue.
    body_fn: The body of the while loop.
    scope: The scope(s) which should be lifted into the loop.
    init: The initial state passed to the loop
    carry_variables: collections that are carried through the loop
      and are therefore mutable (default: none).
    broadcast_variables: collections that are closed over and are
      therefore read-only (default: all collections)
    split_rngs: Split PRNG sequences will be different for each loop iterations.
      If split is False the PRNGs will be the same across iterations.
  Returns:
    The final state after executing the while loop.
  """
  rng_groups, rng_splits = _unzip2(split_rngs.items())

  def inner(scope_fn, repack_fn, variable_groups, rng_groups):
    carry_variables, broadcast_variables = variable_groups

    def make_loop_rngs(i):
      local_rng_groups = []
      for rng_group, rng_split in zip(rng_groups, rng_splits):
        if rng_split:
          rng_group = tree_map_rngs(
            lambda rng: random.fold_in(rng, i), rng_group
          )
        local_rng_groups.append(rng_group)
      return local_rng_groups

    def cond_wrapper(c):
      i, carry_variables, carry = c
      scope = scope_fn(
        (carry_variables, broadcast_variables),
        make_loop_rngs(-i),
        mutable_filter=False,
      )
      return cond_fn(scope, carry)

    def body_wrapper(c):
      i, carry_variables, carry = c
      scope = scope_fn(
        (carry_variables, broadcast_variables), make_loop_rngs(i)
      )
      carry = body_fn(scope, carry)
      (carry_variables,) = repack_fn(scope)
      return (i + 1, carry_variables, carry)

    c = (0, carry_variables, init)
    _, carry_variables, carry = jax.lax.while_loop(
      cond_wrapper, body_wrapper, c
    )
    return carry, (carry_variables,)

  return pack(
    inner,
    (carry_variables, broadcast_variables),
    (carry_variables,),
    rng_groups,
    name='while_loop',
  )(scope)


def while_loop(
  cond_fn: Callable[[ModuleT, C], bool],
  body_fn: Callable[[ModuleT, C], C],
  mdl: ModuleT,
  init: C,
  carry_variables: CollectionFilter = False,
  broadcast_variables: CollectionFilter = True,
  split_rngs: Mapping[PRNGSequenceFilter, bool] = FrozenDict(),
) -> C:
  """Lifted version of jax.lax.while_loop.

  The lifted scope is passed to ``cond_fn`` and ``body_fn``.
  Broadcasted variables are immutable. The carry variable are
  mutable but cannot change shape and dtype.
  This also means you cannot initialize variables inside
  the body. Consider calling ``body_fn`` once manually before
  calling ``while_loop`` if variable initialization is required.

  Example::

    >>> import flax.linen as nn
    >>> import jax, jax.numpy as jnp

    >>> class WhileLoopExample(nn.Module):
    ...   @nn.compact
    ...   def __call__(self, x):
    ...     def cond_fn(mdl, c):
    ...       return mdl.variables['state']['acc'] < 10
    ...     def body_fn(mdl, c):
    ...       acc = mdl.variable('state', 'acc', lambda: jnp.array(0))
    ...       acc.value += 1
    ...       y = nn.Dense(c.shape[-1])(c)
    ...       return y
    ...     c = x
    ...     if self.is_mutable_collection('params'):
    ...       return body_fn(self, c)
    ...     else:
    ...       return nn.while_loop(cond_fn, body_fn, self, c,
    ...                             carry_variables='state')

    >>> k = jax.random.key(0)
    >>> x = jnp.ones((2, 2))
    >>> initial_vars = WhileLoopExample().init(k, x)
    >>> result, state = WhileLoopExample().apply(initial_vars, x, mutable=['state'])

  Args:
    cond_fn: Should return True as long as the loop should continue.
    body_fn: The body of the while loop.
    mdl: The Module which should be lifted into the loop.
    init: The initial state passed to the loop
    carry_variables: collections that are carried through the loop
      and are therefore mutable (default: none).
    broadcast_variables: collections that are closed over and are
      therefore read-only (default: all collections)
    split_rngs: Split PRNG sequences will be different for each loop iterations.
      If split is False the PRNGs will be the same across iterations.
  Returns:
    The final state after executing the while loop.
  """
  return lift_direct_transform(
    lift.while_loop,
    (cond_fn, body_fn),
    mdl,
    init,
    carry_variables,
    broadcast_variables,
    split_rngs,
  )


def while_loop(cond_fun: tp.Callable[[T], tp.Any],
               body_fun: tp.Callable[[T], T],
               init_val: T,
               *,
               graph: bool | None = None,
               graph_updates: bool | None = None) -> T:
  """A Flax NNX transformation of `jax.lax.while_loop <https://jax.readthedocs.io/en/latest/_autosummary/jax.lax.while_loop.html>`_.

  Caution: for the NNX internal reference tracing mechanism to work, you cannot
  change the variable reference structure of ``init_val`` inside ``body_fun``.

  Example::

    >>> import jax
    >>> from flax import nnx
    >>> def fwd_fn(input):
    ...   module, x, count = input
    ...   return module, module(x), count - 1.0

    >>> module = nnx.Linear(10, 10, rngs=nnx.Rngs(0))
    >>> x = jax.random.normal(jax.random.key(0), (10,))
    >>> # `module` will be called three times
    >>> _, y, _ = nnx.while_loop(
    ...   lambda input: input[-1] > 0, fwd_fn, (module, x, 3.0))


  Args:
    cond_fun: A function for the continue condition of the while loop, taking a
      single input of type ``T`` and outputting a boolean.
    body_fun: A function that takes an input of type ``T`` and outputs an ``T``.
      Note that both data and modules of ``T`` must have the same reference
      structure between inputs and outputs.
    init_val: The initial input for ``cond_fun`` and ``body_fun``. Must be of type ``T``.
    graph: if True, use graph-mode (default). If False, use tree-mode.
      If None, uses the value of ``nnx_graph_mode`` config.
    graph_updates: If ``True``, propagates updates on graph structure
      that happen inside the transform to the input graphs, has no
      effect when ``graph=False``.

  """
  if graph is None:
    graph = graphlib.set_graph_mode.current_value()
  if graph_updates is None:
    graph_updates = graphlib.set_graph_updates.current_value()
  if not graph or not graph_updates:
    simple_body_fn = SimpleWhileLoopBodyFn(body_fun, graph=graph)
    simple_cond_fn = SimpleWhileLoopCondFn(cond_fun, graph=graph)

    if graph:
      init_val = extract.to_tree2(init_val)
    val_out = jax.lax.while_loop(simple_cond_fn, simple_body_fn, init_val)
    val_out = extract.update_carry_variables(init_val, val_out)
    if graph:
      val_out = extract.from_tree2(val_out)
    return val_out

  pure_init_val = extract.to_tree(init_val, ctxtag='while_loop')

  pure_init_val = _add_fake_index_mapping(pure_init_val)

  pure_out = jax.lax.while_loop(
    WhileLoopCondFn(cond_fun),
    WhileLoopBodyFn(body_fun),
    pure_init_val,
  )
  out = extract.from_tree(pure_out, ctxtag='while_loop', is_inner=False)
  return out

