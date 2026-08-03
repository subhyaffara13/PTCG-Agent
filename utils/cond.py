import functools
from typing import Any, Callable
import math


def cond(
    pred: bool | int | float | torch.Tensor,
    true_fn: Callable,
    false_fn: Callable,
    operands: tuple | list = (),
) -> Any:
    r"""
    Conditionally applies `true_fn` or `false_fn`.

    .. warning::

        `torch.cond` is a prototype feature in PyTorch. It has limited support for input and output types.
        Please look forward to a more stable implementation in a future version of PyTorch.
        Read more about feature classification at: https://pytorch.org/blog/pytorch-feature-classification-changes/#prototype

    `cond` is structured control flow operator. That is, it is like a Python if-statement,
    but has restrictions on `true_fn`, `false_fn`, and `operands` that enable it to be
    capturable using torch.compile and torch.export.

    Assuming the constraints on `cond`'s arguments are met, `cond` is equivalent to the following::

        def cond(pred, true_branch, false_branch, operands):
            if pred:
                return true_branch(*operands)
            else:
                return false_branch(*operands)

    Args:
        pred (Union[bool, torch.Tensor]): A boolean expression or a tensor with one element,
          indicating which branch function to apply.

        true_fn (Callable): A callable function (a -> b) that is within the
          scope that is being traced.

        false_fn (Callable): A callable function (a -> b) that is within the
          scope that is being traced. The true branch and false branch must
          have consistent input and outputs, meaning the inputs have to be
          the same, and the outputs have to be the same type and shape. Int
          output is also allowed. We'll make the output dynamic by turning it
          into a symint.

        operands (Tuple of possibly nested dict/list/tuple of torch.Tensor): A tuple of inputs to the
          true/false functions. It can be empty if true_fn/false_fn doesn't require input. Defaults to ().

    Example::

        def true_fn(x: torch.Tensor):
            return x.cos()


        def false_fn(x: torch.Tensor):
            return x.sin()


        return cond(x.shape[0] > 4, true_fn, false_fn, (x,))

    Restrictions:
        - The conditional statement (aka `pred`) must meet one of the following constraints:

          - It's a `torch.Tensor` with only one element, and torch.bool dtype

          - It's a boolean expression, e.g. `x.shape[0] > 10` or `x.dim() > 1 and x.shape[1] > 10`

        - The branch function (aka `true_fn`/`false_fn`) must meet all of the following constraints:

          - The function signature must match with operands.

          - The function must return a tensor with the same metadata, e.g. shape,
            dtype, etc.

          - The function cannot have in-place mutations on global variables.
            (Note: in-place tensor operations such as `add_` for intermediate results
            are allowed in a branch)

          - The function can perform in-place mutations on its input tensors during inference (i.e.,
            when `torch.is_grad_enabled()` is False).
            Note: When using `torch.compile()` with a non-constant predicate, the outputs will always
            be new tensors that do not share object identity with the original inputs.

            Example::

                def true_fn(x):
                    return x.sin_()


                def false_fn(x):
                    return x + 1


                def f(x):
                    return cond(x.sum() > 0, true_fn, false_fn, (x,))


                x = torch.ones(4)
                with torch.no_grad():
                    result = torch.compile(f)(x)
                assert result is not x  # result is a new tensor, not the original x

    """
    if torch.compiler.is_dynamo_compiling():
        return cond_op(pred, true_fn, false_fn, operands)

    if isinstance(pred, (bool, int, float)):
        # This is the non-strict export case. Strict export and torch.compile are
        # handled above in dynamo.
        if torch.compiler.is_compiling():
            warnings.warn(
                "Pred is a Python constant. When used with torch.cond, it specializes on one of the branches."
                " If you want torch.cond to preserve two branches, please make the predicate a boolean tensor or a SymBool.",
                UserWarning,
                stacklevel=2,
            )
        # This is the eager case. We can just run the true or false branch.
        if pred:
            return true_fn(*operands)
        else:
            return false_fn(*operands)

    def _validate_input(pred, true_fn, false_fn, operands):
        if not isinstance(pred, (bool, torch.Tensor, torch.SymBool)):
            raise RuntimeError(f"Expected pred to be bool or tensor, but got {pred}.")

        if isinstance(pred, torch.Tensor) and pred.numel() != 1:
            raise RuntimeError(
                f"Expected pred to be bool or single-element tensor, but got {pred}."
            )

        if not callable(true_fn) or not callable(false_fn):
            raise RuntimeError("Expect both branches to be callable.")

        if not isinstance(operands, (tuple, list)) or pytree.tree_any(
            lambda t: not isinstance(t, torch.Tensor), operands
        ):
            raise RuntimeError(
                "Expect operands to be a tuple of possibly nested dict/list/tuple that only "
                f"consists of tensor leaves, but got {operands}."
            )

    _validate_input(pred, true_fn, false_fn, operands)

    if not torch._dynamo.is_dynamo_supported():
        raise RuntimeError("torch.cond requires dynamo support.")

    # Dynamo is expecting a callable with "__code__" attribute.
    # We cannot directly pass cond_op to it. So we wrap it in a dummy function.
    def _cond_op_wrapper(*args, **kwargs):
        return cond_op(*args, **kwargs)

    from torch._higher_order_ops.utils import _hop_compile_and_call

    return _hop_compile_and_call(_cond_op_wrapper, (pred, true_fn, false_fn, operands))


def cond(
    pred, true_fn, false_fn, operands
) -> list[ir.TensorBox | ir.ShapeAsConstantBuffer]:
    # TODO: when graph_partition is enabled, skip - partitioning handles control flow
    # we run into memory cleanup issue
    if any(isinstance(x, IRNode) and is_triton(x) for x in [pred, *operands]):
        msg = "control flow operator: torch.cond."
        if stack_trace := V.graph.current_node.meta.get("stack_trace", None):
            msg = f"{msg} Found from : \n {stack_trace}"
        V.graph.disable_cudagraphs_reason = msg

    result = ir.Conditional.create(pred, true_fn, false_fn, operands)
    return list(map(TensorBox.create, result))  # pyrefly: ignore no-matching-overload


def cond(x: ArrayLike, p=None):
    x = _atleast_float_1(x)

    # check if empty
    # cf: https://github.com/numpy/numpy/blob/v1.24.0/numpy/linalg/linalg.py#L1744
    if x.numel() == 0 and math.prod(x.shape[-2:]) == 0:
        raise LinAlgError("cond is not defined on empty arrays")

    result = torch.linalg.cond(x, p=p)

    # Convert nans to infs (numpy does it in a data-dependent way, depending on
    # whether the input array has nans or not)
    # XXX: NumPy does this: https://github.com/numpy/numpy/blob/v1.24.0/numpy/linalg/linalg.py#L1744
    return torch.where(torch.isnan(result), float("inf"), result)


def cond(x, p=None):
    """
    Compute the condition number of a matrix.

    This function is capable of returning the condition number using
    one of seven different norms, depending on the value of `p` (see
    Parameters below).

    Parameters
    ----------
    x : (..., M, N) array_like
        The matrix whose condition number is sought.
    p : {None, 1, -1, 2, -2, inf, -inf, 'fro'}, optional
        Order of the norm used in the condition number computation:

        =====  ============================
        p      norm for matrices
        =====  ============================
        None   2-norm, computed directly using the ``SVD``
        'fro'  Frobenius norm
        inf    max(sum(abs(x), axis=1))
        -inf   min(sum(abs(x), axis=1))
        1      max(sum(abs(x), axis=0))
        -1     min(sum(abs(x), axis=0))
        2      2-norm (largest sing. value)
        -2     smallest singular value
        =====  ============================

        inf means the `numpy.inf` object, and the Frobenius norm is
        the root-of-sum-of-squares norm.

    Returns
    -------
    c : {float, inf}
        The condition number of the matrix. May be infinite.

    See Also
    --------
    numpy.linalg.norm

    Notes
    -----
    The condition number of `x` is defined as the norm of `x` times the
    norm of the inverse of `x` [1]_; the norm can be the usual L2-norm
    (root-of-sum-of-squares) or one of a number of other matrix norms.

    References
    ----------
    .. [1] G. Strang, *Linear Algebra and Its Applications*, Orlando, FL,
           Academic Press, Inc., 1980, pg. 285.

    Examples
    --------
    >>> import numpy as np
    >>> from numpy import linalg as LA
    >>> a = np.array([[1, 0, -1], [0, 1, 0], [1, 0, 1]])
    >>> a
    array([[ 1,  0, -1],
           [ 0,  1,  0],
           [ 1,  0,  1]])
    >>> LA.cond(a)
    1.4142135623730951
    >>> LA.cond(a, 'fro')
    3.1622776601683795
    >>> LA.cond(a, np.inf)
    2.0
    >>> LA.cond(a, -np.inf)
    1.0
    >>> LA.cond(a, 1)
    2.0
    >>> LA.cond(a, -1)
    1.0
    >>> LA.cond(a, 2)
    1.4142135623730951
    >>> LA.cond(a, -2)
    0.70710678118654746 # may vary
    >>> (min(LA.svd(a, compute_uv=False)) *
    ... min(LA.svd(LA.inv(a), compute_uv=False)))
    0.70710678118654746 # may vary

    """
    x = asarray(x)  # in case we have a matrix
    if _is_empty_2d(x):
        raise LinAlgError("cond is not defined on empty arrays")
    if p is None or p in {2, -2}:
        s = svd(x, compute_uv=False)
        with errstate(all='ignore'):
            if p == -2:
                r = s[..., -1] / s[..., 0]
            else:
                r = s[..., 0] / s[..., -1]
    else:
        # Call inv(x) ignoring errors. The result array will
        # contain nans in the entries where inversion failed.
        _assert_stacked_square(x)
        t, result_t = _commonType(x)
        result_t = _realType(result_t)  # condition number is always real
        signature = 'D->D' if isComplexType(t) else 'd->d'
        with errstate(all='ignore'):
            invx = _umath_linalg.inv(x, signature=signature)
            r = norm(x, p, axis=(-2, -1)) * norm(invx, p, axis=(-2, -1))
        r = r.astype(result_t, copy=False)

    # Convert nans to infs unless the original array had nan entries
    nan_mask = isnan(r)
    if nan_mask.any():
        nan_mask &= ~isnan(x).any(axis=(-2, -1))
        if r.ndim > 0:
            r[nan_mask] = inf
        elif nan_mask:
            # Convention is to return scalars instead of 0d arrays.
            r = r.dtype.type(inf)

    return r


def cond(x: ArrayLike, p=None):
  """Compute the condition number of a matrix.

  JAX implementation of :func:`numpy.linalg.cond`.

  The condition number is defined as ``norm(x, p) * norm(inv(x), p)``. For ``p = 2``
  (the default), the condition number is the ratio of the largest to the smallest
  singular value.

  Args:
    x: array of shape ``(..., M, N)`` for which to compute the condition number.
    p: the order of the norm to use. One of ``{None, 1, -1, 2, -2, inf, -inf, 'fro'}``;
      see :func:`jax.numpy.linalg.norm` for the meaning of these. The default is ``p = None``,
      which is equivalent to ``p = 2``. If not in ``{None, 2, -2}`` then ``x`` must be square,
      i.e. ``M = N``.

  Returns:
    array of shape ``x.shape[:-2]`` containing the condition number.

  See also:
    :func:`jax.numpy.linalg.norm`

  Examples:

    Well-conditioned matrix:

    >>> x = jnp.array([[1, 2],
    ...                [2, 1]])
    >>> jnp.linalg.cond(x)
    Array(3., dtype=float32)

    Ill-conditioned matrix:

    >>> x = jnp.array([[1, 2],
    ...                [0, 0]])
    >>> jnp.linalg.cond(x)
    Array(inf, dtype=float32)
  """
  arr = ensure_arraylike("cond", x)
  if arr.ndim < 2:
    raise ValueError(f"jnp.linalg.cond: input array must be at least 2D; got {arr.shape=}")
  if arr.shape[-1] == 0 or arr.shape[-2] == 0:
    raise ValueError(f"jnp.linalg.cond: input array must not be empty; got {arr.shape=}")
  if p is None or p == 2:
    s = svdvals(x)
    return s[..., 0] / s[..., -1]
  elif p == -2:
    s = svdvals(x)
    r = s[..., -1] / s[..., 0]
  else:
    if arr.shape[-2] != arr.shape[-1]:
      raise ValueError(f"jnp.linalg.cond: for {p=}, array must be square; got {arr.shape=}")
    r = norm(x, ord=p, axis=(-2, -1)) * norm(inv(x), ord=p, axis=(-2, -1))
  # Convert NaNs to infs where original array has no NaNs.
  return jnp.where(ufuncs.isnan(r) & ~ufuncs.isnan(x).any(axis=(-2, -1)), np.inf, r)


def cond(pred, true_fun: Callable, false_fun: Callable, *operands,
          operand=_no_operand_sentinel):
  """Conditionally apply ``true_fun`` or ``false_fun``.

  Wraps XLA's `Conditional
  <https://www.openxla.org/xla/operation_semantics#conditional>`_
  operator.

  Provided arguments are correctly typed, ``cond()`` has equivalent
  semantics to this Python implementation, where ``pred`` must be a
  scalar type::

    def cond(pred, true_fun, false_fun, *operands):
      if pred:
        return true_fun(*operands)
      else:
        return false_fun(*operands)


  In contrast with :func:`jax.lax.select`, using ``cond`` indicates that only one of
  the two branches is executed (up to compiler rewrites and optimizations).
  However, when transformed with :func:`~jax.vmap` to operate over a batch of
  predicates, ``cond`` is converted to :func:`~jax.lax.select`.
  Both branches will be traced in all cases (see :ref:`Key concepts: tracing <key-concepts-tracing>`
  for a discussion of JAX's tracing model).

  Args:
    pred: Boolean scalar type, indicating which branch function to apply.
    true_fun: Function (A -> B), to be applied if ``pred`` is True.
    false_fun: Function (A -> B), to be applied if ``pred`` is False.
    operands: Operands (A) input to either branch depending on ``pred``. The
      type can be a scalar, array, or any pytree (nested Python tuple/list/dict)
      thereof.

  Returns:
    Value (B) of either ``true_fun(*operands)`` or ``false_fun(*operands)``,
    depending on the value of ``pred``. The type can be a scalar, array, or any
    pytree (nested Python tuple/list/dict) thereof.
  """
  if not (callable(true_fun) and callable(false_fun)):
    # try falling back to the old, deprecated version of `cond`
    if callable(false_fun) and len(operands) == 2 and callable(operands[1]):
      x_true, f_true, x_false, f_false = true_fun, false_fun, *operands
      return cond(pred, lambda x, _: f_true(x), lambda _, x: f_false(x), x_true, x_false)
    else:
      raise TypeError("lax.cond: true_fun and false_fun arguments should be callable.")
  if operand is not _no_operand_sentinel:
    if operands:
      raise TypeError("if 'operand' keyword is passed then no positional "
                      f"operands can be passed, got {operand=} "
                      f"and positional operands {operands}")
    operands = (operand,)
  del operand

  if pred is None:
    raise TypeError("cond predicate is None")
  if isinstance(pred, Sequence) or np.ndim(pred) != 0:
    raise TypeError(
        f"Pred must be a scalar, got {pred} of " +
        (f"type {type(pred)}" if isinstance(pred, Sequence)
         else f"shape {np.shape(pred)}."))

  try:
    pred_dtype = dtypes.result_type(pred)
  except TypeError as err:
    msg = ("Pred type must be either boolean or number, got {}.")
    raise TypeError(msg.format(pred)) from err

  if pred_dtype.kind != 'b':
    if pred_dtype.kind in 'iuf':
      pred = pred != 0
    else:
      msg = ("Pred type must be either boolean or number, got {}.")
      raise TypeError(msg.format(pred_dtype))

  if config.disable_jit.value and core.is_concrete(pred):
    if pred:
      return true_fun(*operands)
    else:
      return false_fun(*operands)

  args = FlatTree.flatten((operands, {}))
  dbg_true = api_util.debug_info("cond", true_fun, operands, {})
  api_util.check_no_transformed_refs_args(lambda: dbg_true, args.vals)
  avals = args.map(core.typeof)
  avals = avals.map2(
      lambda a, x: core.AvalQDD(a, cur_qdd(x)) if a.has_qdd else a,
      list(args))
  if config.mutable_array_checks.value:
    api_util.check_no_aliased_ref_args(lambda: dbg_true, list(avals), list(args))
  dbg_false = api_util.debug_info("cond", false_fun, operands, {})

  true_jaxpr_, out_avals = pe.trace_to_jaxpr(true_fun, avals, dbg_true)
  true_jaxpr_, true_consts = pe.separate_consts(true_jaxpr_)
  false_jaxpr_, false_out_avals = pe.trace_to_jaxpr(false_fun, avals, dbg_false)
  false_jaxpr_, false_consts = pe.separate_consts(false_jaxpr_)
  (true_jaxpr, false_jaxpr), consts = _merge_common_consts(
      (true_jaxpr_, false_jaxpr_), (true_consts, false_consts))
  if config.mutable_array_checks.value:
    api_util._check_no_aliased_closed_over_refs(
        dbg_true, (*true_jaxpr.consts, *consts), list(args))

  if any(isinstance(out_aval, AbstractRef) for out_aval in
         true_jaxpr.out_avals + false_jaxpr.out_avals):
    raise ValueError("Cannot return `Ref`s from `cond`.")

  _check_branch_outputs(
      'cond', 'true_fun', 'false_fun',
      true_fun, false_fun, out_avals, false_out_avals)

  # prune passthrough outputs
  true_fwds = pe._jaxpr_forwarding(true_jaxpr.jaxpr)
  false_fwds = pe._jaxpr_forwarding(false_jaxpr.jaxpr)
  in_fwd = [i if i == j else None for i, j in zip(true_fwds, false_fwds)]
  keep = [f is None for f in in_fwd]
  true_jaxpr = pe.prune_closed_jaxpr_outputs(true_jaxpr, keep)
  false_jaxpr = pe.prune_closed_jaxpr_outputs(false_jaxpr, keep)

  joined_effects = core.join_effects(core.positional_effects(true_jaxpr),
                                     core.positional_effects(false_jaxpr))
  disallowed_effects = effects.control_flow_allowed_effects.filter_not_in(joined_effects)
  if disallowed_effects:
    raise NotImplementedError(
        f'Effects not supported in `cond`: {disallowed_effects}')

  index = lax.convert_element_type(pred, np.int32)
  false_jaxpr = replace_jaxpr_effects(
      false_jaxpr,
      core.resolve_input_effects(joined_effects, false_jaxpr.jaxpr.invars))
  true_jaxpr = replace_jaxpr_effects(
      true_jaxpr,
      core.resolve_input_effects(joined_effects, true_jaxpr.jaxpr.invars))

  out = cond_p.bind(index, *consts, *args, branches=(false_jaxpr, true_jaxpr))
  out_ = iter(out)

  all_inputs = [*consts, *args]
  out = [
    next(out_) if fwd is None else lax.asarray(all_inputs[fwd])
    for fwd in in_fwd
  ]
  assert next(out_, None) is None
  return out_avals.update(out).unflatten()


def cond(
  pred: Any,
  true_fun: Callable[..., C],
  false_fun: Callable[..., C],
  scope: Scope,
  *operands,
  variables: CollectionFilter = True,
  rngs: PRNGSequenceFilter = True,
) -> C:
  """Lifted version of ``jax.lax.cond``.

  The returned values from ``true_fun`` and ``false_fun``
  must have the same Pytree structure, shapes, and dtypes.
  The variables created or updated inside the
  branches must also have the same structure.
  Note that this constraint is violated when
  creating variables or submodules in only one branch.
  Because initializing variables in just one branch
  causes the parameter structure to be different.

  Example::

    def cond_example(scope, x, pred):
      scope.variable('state', 'true_count', lambda: 0)
      scope.variable('state', 'false_count', lambda: 0)
      def true_fn(scope, x):
        scope.variable('state', 'true_count').value += 1
        return scope.child(nn.dense)(x, 2)
      def false_fn(scope, x):
        scope.variable('state', 'false_count').value += 1
        return -scope.child(nn.dense)(x, 2)
      return lift.cond(pred, true_fn, false_fn, scope, x)


  Args:
    pred: determines if true_fun or false_fun is evaluated.
    true_fun: The function evalauted when ``pred`` is `True`.
      The signature is (Scope, *operands) -> T.
    false_fun: The function evalauted when ``pred`` is `False`.
      The signature is (Scope, *operands) -> T.
    scope: A Scope or Pytree of scopes to pass
    *operands: The arguments passed to ``true_fun`` and ``false_fun``
    variables: The variable collections passed to the conditional
      branches (default: all)
    rngs: The PRNG sequences passed to the conditionals (default: all)
  Returns:
    The result of the evaluated branch (``true_fun`` or ``false_fun``).
  """
  branches = [true_fun, false_fun]

  def inner(scope_fn, repack_fn, variable_groups, rng_groups):
    def branch_wrapper(branch_fn, *operands):
      scope = scope_fn(variable_groups, rng_groups)
      y = branch_fn(scope, *operands)
      return y, repack_fn(scope)

    pure_branches = [
      functools.partial(branch_wrapper, branch_fn) for branch_fn in branches
    ]
    return jax.lax.cond(pred, pure_branches[0], pure_branches[1], *operands)

  return pack(inner, (variables,), (variables,), (rngs,), name='cond')(scope)


def cond(
  pred: Any,
  true_fun: Callable[..., C],
  false_fun: Callable[..., C],
  mdl: Module,
  *operands,
  variables: CollectionFilter = True,
  rngs: PRNGSequenceFilter = True,
) -> C:
  """Lifted version of ``jax.lax.cond``.

  The returned values from ``true_fun`` and ``false_fun``
  must have the same Pytree structure, shapes, and dtypes.
  The variables created or updated inside the
  branches must also have the same structure.
  Note that this constraint is violated when
  creating variables or submodules in only one branch.
  Because initializing variables in just one branch
  causes the parameter structure to be different.

  Example::

    >>> import flax.linen as nn

    >>> class CondExample(nn.Module):
    ...   @nn.compact
    ...   def __call__(self, x, pred):
    ...     self.variable('state', 'true_count', lambda: 0)
    ...     self.variable('state', 'false_count', lambda: 0)
    ...     def true_fn(mdl, x):
    ...       mdl.variable('state', 'true_count').value += 1
    ...       return nn.Dense(2, name='dense')(x)
    ...     def false_fn(mdl, x):
    ...       mdl.variable('state', 'false_count').value += 1
    ...       return -nn.Dense(2, name='dense')(x)
    ...     return nn.cond(pred, true_fn, false_fn, self, x)

  Args:
    pred: determines if true_fun or false_fun is evaluated.
    true_fun: The function evaluated when ``pred`` is ``True``.
      The signature is (module, *operands) -> T.
    false_fun: The function evaluated when ``pred`` is ``False``.
      The signature is (module, *operands) -> T.
    mdl: A Module target to pass.
    *operands: The arguments passed to ``true_fun`` and ``false_fun``
    variables: The variable collections passed to the conditional
      branches (default: all)
    rngs: The PRNG sequences passed to the conditionals (default: all)
  Returns:
    The result of the evaluated branch (``true_fun`` or ``false_fun``).
  """
  return lift_direct_transform(
    _cond_wrapper,
    (true_fun, false_fun),
    mdl,
    pred,
    *operands,
    variables=variables,
    rngs=rngs,
  )


def cond(
  pred,
  true_fun: tp.Callable[..., A],
  false_fun: tp.Callable[..., A],
  *operands,
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> A:
  """Conditionally apply ``true_fun`` or ``false_fun``.

  Wraps `jax.lax.cond <https://jax.readthedocs.io/en/latest/_autosummary/jax.lax.cond.html>`__
  to support Flax NNX modules and variables.

  Args:
    pred: boolean scalar. If True, ``true_fun`` is applied, otherwise
      ``false_fun``.
    true_fun: function to apply if ``pred`` is True.
    false_fun: function to apply if ``pred`` is False.
    *operands: operands passed to whichever branch is selected.
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
    extract.check_no_aliases('cond', operands=operands)
    out, updates = jax.lax.cond(
      pred,
      SimpleCondFn(true_fun, graph=graph),
      SimpleCondFn(false_fun, graph=graph),
      *operands,
    )
    if graph:
      out = extract.from_tree2(out)
    extract.apply_variable_updates(operands, updates)
    return out

  @general.split_inputs(ctxtag='cond')
  def _cond(pred, true_fun, false_fun, *operands):
    return jax.lax.cond(
      pred,
      general.merge_inputs(true_fun, ctxtag='cond'),
      general.merge_inputs(false_fun, ctxtag='cond'),
      *operands,
    )

  return _cond(pred, true_fun, false_fun, *operands)

