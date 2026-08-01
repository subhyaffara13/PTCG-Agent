
def scan(stream, Loader=Loader):
    """
    Scan a YAML stream and produce scanning tokens.
    """
    loader = Loader(stream)
    try:
        while loader.check_token():
            yield loader.get_token()
    finally:
        loader.dispose()


def scan(
    combine_fn: Callable[
        [pytree.PyTree, pytree.PyTree], tuple[pytree.PyTree, pytree.PyTree]
    ],
    init: pytree.PyTree,
    xs: pytree.PyTree,
    *,
    dim: int = 0,
    reverse: bool = False,
) -> tuple[pytree.PyTree, pytree.PyTree]:
    r"""
    Performs an inclusive scan with a combine function.

    .. warning::

        ``torch.scan`` is a prototype feature in PyTorch. You may run into miscompiles.
        Read more about feature classification at:
        https://pytorch.org/blog/pytorch-feature-classification-changes/#prototype

    Args:
        combine_fn (Callable): A binary callable with type ``(Tensor, Tensor) -> (Tensor, Tensor)``,
            or if xs is a pytree ``(pytree, pytree) -> (pytree, pytree)``.
            The first input to ``combine_fn`` is the previous or initial scan carry
            and the second input element to ``combine_fn`` is a slice of the input along dim.
            The first output element of ``combine_fn`` is the next scan carry
            and the second output  of ``combine_fn`` represents a slice of the output.
            This function must be pure, i.e., no lifted arguments are supported at the moment
            and may not have any side effects.
        init (torch.Tensor or pytree with tensor leaves): The initial scan carry, a tensor, or nested pytree of tensors.
            The ``init`` is expected to have the same pytree structure as the first output element (i.e. carry)
            of ``combine_fn``.
        xs (torch.Tensor or pytree with tensor leaves): The input tensor, or nested pytree of tensors.

    Kwargs:
        dim (int): the dimension to scan over, default 0.
        reverse (bool): A boolean stating if the scan should be reversed with respect to ``dim``, default ``False``.

    Returns:
        final_carry (torch.Tensor or pytree with tensor leaves),
            the final carry of the scan operation with same pytree structure as init.
        out (torch.Tensor or pytree with tensor leaves),
            each tensor leaf is a stacked output along first dim, where each slice is the output of a scan iteration.

    Restrictions:
        - The combine_fn shouldn't have any aliasing between input-input, input-output, and output-output. E.g. return a view
            or the same tensor as input is not supported. As a workaround, can clone the output to avoid aliasing.

        - The combine_fn shouldn't mutate any inputs. We'll remove the mutation restriction for inference soon. Please file an issue
            if you input mutation support for training is needed.

        - The combine_fn's init carry should match the next_carry in pytree structure and in tensor metadata.

    Example::

        def add(x: torch.Tensor, y: torch.Tensor):
            next_carry = y = x + y
            # clone the output to avoid output-output aliasing
            return next_carry, y.clone()


        i0 = torch.zeros(1)
        xs = torch.arange(5)
        # returns torch.tensor([10.]), torch.tensor([[0], [1.], [3.], [6.], [10.]])
        last_carry, cumsum = scan(add, init=i0, xs=xs)


    """
    # The reason we flatten init and xs before calling into dynamo is that
    # we want to create a consistent input ordering for combine_fn
    # and we also want to the input ordering matches the output ordering.
    leaves_init, spec_init = pytree.tree_flatten(init)
    leaves_xs_orig, spec_xs = pytree.tree_flatten(xs)

    # Shortcut if no xs is provided
    if len(leaves_xs_orig) == 0:
        return init, []

    def _validate_input(cfn, lxs, linit, d, r):
        # Basic arguments check
        if not callable(cfn):
            raise RuntimeError(f"Combine_fn must be a callable, but got {cfn}")
        if not isinstance(d, int):
            raise RuntimeError("Dim must be an int, but got " + str(type(d)))
        if not isinstance(r, bool):
            raise RuntimeError("Reverse must be a bool, but got " + str(type(r)))

        # Checks for init
        if len(linit) == 0:
            raise RuntimeError("scan() operator requires init leaves.")
        for x in linit:
            if not isinstance(x, torch.Tensor):
                raise RuntimeError(f"All init leaves must be a Tensor but got {x}")

        # Checks for xs
        for x in lxs:
            if not isinstance(x, torch.Tensor):
                raise RuntimeError(f"All xs leaves must be a Tensor but got {x}")
        if any(x.ndim <= d for x in lxs):
            raise RuntimeError(
                "All xs leaves must at least have 'dim' number of dimensions and scan dimension > 0"
            )
        if any(x.shape[d] == 0 for x in lxs):
            raise RuntimeError(
                "All xs leaves must at least have 'dim' number of dimensions and scan dimension > 0"
            )

    ndim = leaves_xs_orig[0].ndim
    dim = utils.canonicalize_dim(ndim, dim)

    _validate_input(combine_fn, leaves_xs_orig, leaves_init, dim, reverse)

    # Move scan dim to 0 and always perform scan on dim 0
    leaves_xs = []
    for elem in leaves_xs_orig:
        leaves_xs.append(torch.movedim(elem, dim, 0) if dim != 0 else elem)

    if reverse:
        leaves_xs = [torch.flip(elem, [0]) for elem in leaves_xs]

    # TODO: Support _inductor lowering
    # TODO: Unify handling of pytrees for control flow ops, such as cond, while_loop, etc.

    combine_fn = functools.partial(
        wrap_combine_fn_flat,
        combine_fn=combine_fn,
        spec_init=spec_init,
        spec_xs=spec_xs,
        num_init_leaves=len(leaves_init),
        num_inp_leaves=len(leaves_xs),
    )

    def run_flattened_scan(combine_fn, leaves_init, leaves_xs):
        return scan_op(combine_fn, leaves_init, leaves_xs, additional_inputs=())

    carry, out = _maybe_compile_and_run_fn(
        run_flattened_scan,
        combine_fn,
        leaves_init,
        leaves_xs,
    )

    if reverse:
        out = pytree.tree_map(lambda elem: elem.flip([0]), out)

    return carry, out


def scan(result: _Sequence[_ods_ir.Type], srcs: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], axis: _Union[int, _ods_ir.IntegerAttr], reverse: _Union[bool, _ods_ir.BoolAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, ScanOp]:
  op = ScanOp(result=result, srcs=srcs, axis=axis, reverse=reverse, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def scan(output: _ods_ir.Type, input: _ods_ir.Value[_ods_ir.VectorType], kind: _Union[_Any, _ods_ir.Attribute], *, mask: _Optional[_ods_ir.Value[_ods_ir.VectorType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return ScanOp(output=output, input=input, kind=kind, mask=mask, loc=loc, ip=ip).result


def scan(outputs: _Sequence[_ods_ir.Type], carries: _Sequence[_ods_ir.Type], inputs: _Sequence[_ods_ir.Value], inits: _Sequence[_ods_ir.Value], dimension: _Union[int, _ods_ir.IntegerAttr], *, scan_dim_size: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, is_reverse: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, is_associative: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, ScanOp]:
  op = ScanOp(outputs=outputs, carries=carries, inputs=inputs, inits=inits, dimension=dimension, scan_dim_size=scan_dim_size, is_reverse=is_reverse, is_associative=is_associative, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def scan(outputs: _Sequence[_ods_ir.Type], carries: _Sequence[_ods_ir.Type], inputs: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], inits: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], dimension: _Union[int, _ods_ir.IntegerAttr], *, scan_dim_size: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, is_reverse: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, is_associative: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, ScanOp]:
  op = ScanOp(outputs=outputs, carries=carries, inputs=inputs, inits=inits, dimension=dimension, scan_dim_size=scan_dim_size, is_reverse=is_reverse, is_associative=is_associative, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def scan(kind: _Union[_Any, _ods_ir.Attribute], source: _ods_ir.Value[_ods_ir.VectorType], initial_value: _ods_ir.Value[_ods_ir.VectorType], reduction_dim: _Union[int, _ods_ir.IntegerAttr], inclusive: _Union[bool, _ods_ir.BoolAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResultList:
  return ScanOp(kind=kind, source=source, initial_value=initial_value, reduction_dim=reduction_dim, inclusive=inclusive, results=results, loc=loc, ip=ip).results


def scan(f: Callable[[Carry, X], tuple[Carry, Y]],
         init: Carry,
         xs: X | None = None,
         length: int | None = None,
         reverse: bool = False,
         unroll: int | bool = 1,
         _split_transpose: bool = False) -> tuple[Carry, Y]:
  """Scan a function over leading array axes while carrying along state.

  The `Haskell-like type signature`_ in brief is

  .. code-block:: haskell

    scan :: (c -> a -> (c, b)) -> c -> [a] -> (c, [b])

  where for any array type specifier ``t``, ``[t]`` represents the type with an additional
  leading axis, and if ``t`` is a pytree (container) type with array leaves then ``[t]``
  represents the type with the same pytree structure and corresponding leaves
  each with an additional leading axis.

  When the type of ``xs`` (denoted `a` above) is an array type or None, and the type
  of ``ys`` (denoted `b` above) is an array type, the semantics of :func:`~scan` are
  given roughly by this Python implementation::

    def scan(f, init, xs, length=None):
      if xs is None:
        xs = [None] * length
      carry = init
      ys = []
      for x in xs:
        carry, y = f(carry, x)
        ys.append(y)
      return carry, np.stack(ys)

  Unlike that Python version, both ``xs`` and ``ys`` may be arbitrary pytree
  values, and so multiple arrays can be scanned over at once and produce multiple
  output arrays. ``None`` is actually a special case of this, as it represents an
  empty pytree.

  Also unlike that Python version, :func:`~scan` is a JAX primitive and is
  lowered to a single WhileOp. That makes it useful for reducing
  compilation times for JIT-compiled functions, since native Python
  loop constructs in an :func:`~jax.jit` function are unrolled, leading to large
  XLA computations.

  Finally, the loop-carried value ``carry`` must hold a fixed shape and dtype
  across all iterations (and not just be consistent up to NumPy rank/shape
  broadcasting and dtype promotion rules, for example). In other words, the type
  ``c`` in the type signature above represents an array with a fixed shape and
  dtype (or a nested tuple/list/dict container data structure with a fixed
  structure and arrays with fixed shape and dtype at the leaves).

  .. note::
    :py:func:`scan` compiles ``f``, so while it can be combined with
    :py:func:`jit`, it's usually unnecessary.

  .. note::
    :func:`scan` is designed for iterating with a static number of iterations.
    For iteration with a dynamic number of iterations, use :func:`fori_loop`
    or :func:`while_loop`.

  Args:
    f: a Python function to be scanned of type ``c -> a -> (c, b)``, meaning
      that ``f`` accepts two arguments where the first is a value of the loop
      carry and the second is a slice of ``xs`` along its leading axis, and that
      ``f`` returns a pair where the first element represents a new value for
      the loop carry and the second represents a slice of the output.
    init: an initial loop carry value of type ``c``, which can be a scalar,
      array, or any pytree (nested Python tuple/list/dict) thereof, representing
      the initial loop carry value. This value must have the same structure as
      the first element of the pair returned by ``f``.
    xs: the value of type ``[a]`` over which to scan along the leading axis,
      where ``[a]`` can be an array or any pytree (nested Python
      tuple/list/dict) thereof with consistent leading axis sizes.
    length: optional integer specifying the number of loop iterations, which
      must agree with the sizes of leading axes of the arrays in ``xs`` (but can
      be used to perform scans where no input ``xs`` are needed).
    reverse: optional boolean specifying whether to run the scan iteration
      forward (the default) or in reverse, equivalent to reversing the leading
      axes of the arrays in both ``xs`` and in ``ys``.
    unroll: optional non-negative int or bool specifying, in the underlying
      operation of the scan primitive, how many scan iterations to unroll within
      a single iteration of a loop. If an integer is provided, it determines how
      many unrolled loop iterations to run within a single rolled iteration of
      the loop. `unroll=0` unrolls the entire loop.
      If a boolean is provided, it will determine if the loop is
      completely unrolled (i.e. `unroll=True`) or left completely rolled (i.e.
      `unroll=False`).

  Returns:
    A pair of type ``(c, [b])`` where the first element represents the final
    loop carry value and the second element represents the stacked outputs of
    the second output of ``f`` when scanned over the leading axis of the inputs.

  .. _Haskell-like type signature: https://wiki.haskell.org/Type_signature
  """

  if config.scan3.value:
    return scan3(f, init, xs, length, reverse, unroll)

  if not callable(f):
    raise TypeError("lax.scan: f argument should be a callable.")

  dbg_body = api_util.debug_info("scan", f, (init, xs), {})
  init_flat = FlatTree.flatten(init)
  xs_flat = FlatTree.flatten(xs)
  args = FlatTree.pack((init_flat, xs_flat))
  check_no_transformed_refs_args(lambda: dbg_body, args.vals)
  del init, xs

  args_avals = args.map(core.typeof)
  init_avals, xs_avals = args_avals.unpack()
  length = _infer_scan_length(list(xs_flat), list(xs_avals), length)

  if config.disable_jit.value:
    if length == 0:
      raise ValueError("zero-length scan is not supported in disable_jit() "
                       "mode because the output type is unknown.")
    carry = init_flat.unflatten()
    ys = []
    maybe_reversed = reversed if reverse else lambda x: x
    for i in maybe_reversed(range(length)):
      xs_slice = xs_flat.map(lambda x: slicing.index_in_dim(x, i, keepdims=False))
      carry, y = f(carry, xs_slice.unflatten())
      ys.append(y)
    stack = lambda *ys: _stack(ys)
    stacked_y = tree_map(stack, *maybe_reversed(ys))
    return carry, stacked_y

  if config.mutable_array_checks.value:
    check_no_aliased_ref_args(lambda: dbg_body, list(args_avals), list(args))

  x_avals = xs_avals.map(lambda aval: core.mapped_leading_aval(length, aval))
  def _create_jaxpr(carry_avals):
    new_arg_avals = FlatTree.pack(((carry_avals, x_avals), {}))
    jaxpr, out_avals = pe.trace_to_jaxpr(f, new_arg_avals, dbg_body)
    jaxpr, consts = pe.separate_consts(jaxpr)
    if len(out_avals.unpack()) != 2:
      msg = "scan body output must be a pair, got {}."
      raise TypeError(msg.format(out_avals.unflatten()))
    return jaxpr, out_avals, consts

  # The carry input and output avals must match exactly. However, we want to account for
  # the case when init contains weakly-typed values (e.g. Python scalars), with avals that
  # may not match the output despite being compatible by virtue of their weak type.
  # To do this, we compute the jaxpr in two passes: first with the raw inputs, and if
  # necessary, a second time with modified init values.
  # TODO(dougalm): this two-pass stuff is expensive (exponential in scan nesting
  # depth) and incomplete (because in the general case it takes more than two passes).
  # Let's get rid of it, perhaps after getting rid of weak types altogether.
  jaxpr, out_avals, consts = _create_jaxpr(init_avals)
  if config.mutable_array_checks.value:
    _check_no_aliased_closed_over_refs(dbg_body, consts, list(args))
  carry_out_avals, ys_avals = out_avals.unpack()
  if len(carry_out_avals) != len(init_avals):
    _check_carry_type('scan body', f, init_avals, carry_out_avals)
  init_flat, changed = init_flat.map3(
     _promote_weak_typed_input,
     init_avals, carry_out_avals).unzip2()
  num_carry, num_xs, num_ys = len(init_flat), len(xs_flat), len(ys_avals)
  if any(changed):
    init_avals = init_flat.map(core.typeof)
    jaxpr, out_avals, consts = _create_jaxpr(init_avals)
    carry_out_avals, ys_avals = out_avals.unpack()

  _check_carry_type('scan body', f, init_avals, carry_out_avals)

  disallowed_effects = effects.control_flow_allowed_effects.filter_not_in(jaxpr.effects)
  if disallowed_effects:
    raise NotImplementedError(
        f'Effects not supported in `scan`: {disallowed_effects}')

  unroll = core.concrete_or_error(
      None, unroll,
      "The `unroll` argument to `scan` expects a concrete `int` or `bool` "
      "value.")
  if isinstance(unroll, bool):
    unroll = max(length, 1) if unroll else 1
  if unroll < 0:
    raise ValueError("`unroll` must be a `bool` or a non-negative `int`.")

  args_flat = [*init_flat.vals, *xs_flat.vals]

  # If the body forwards an input carry to an output carry, that input is
  # read-only and can be moved to be a const. Doing so can lead to efficiency
  # wins, e.g. if the scan is inside a cond with a batched predicate.
  num_ys = len(jaxpr.out_avals) - num_carry
  carry_fwd, ext_fwd = split_list(pe._jaxpr_forwarding(jaxpr.jaxpr), [num_carry])
  move_to_const = [len(consts) + i == f for i, f in enumerate(carry_fwd)]
  if any(move_to_const):
    jaxpr = pe.prune_closed_jaxpr_outputs(
        jaxpr, [not m for m in move_to_const] + [True] * num_ys)
    jaxpr = pe.move_binders_to_front(
        jaxpr, [False] * len(consts) + move_to_const + [False] * num_xs)
    args_flat, new_consts = partition_list(move_to_const + [False] * num_xs, args_flat)
    consts = [*new_consts, *consts]
    num_carry -= len(new_consts)
  else:
    new_consts = []

  # When an extensive output is forwarded from an extensive input, we can
  # avoid copying it by pruning it from the jaxpr and forwarding manually. We
  # don't need to update the indexing based on the optimization above since it
  # doesn't change the total number of consts and carries combined, and
  # `ext_fwd` already only includes the extensive outputs. But, we do remove
  # the number of consts from the index since we're going to use it to index
  # into `in_flat`, which doesn't include consts.
  ext_to_ext_fwd = [
      in_idx - len(consts) if in_idx is not None and
      in_idx >= num_carry + len(consts) else None for in_idx in ext_fwd]
  jaxpr = pe.prune_closed_jaxpr_outputs(
      jaxpr, [True] * num_carry + [i is None for i in ext_to_ext_fwd])

  out = scan_p.bind(*consts, *args_flat,
                    reverse=reverse, length=length, jaxpr=jaxpr,
                    num_consts=len(consts), num_carry=num_carry,
                    unroll=unroll)

  # Apply input to output forwarding that was computed above.
  carry_out, out = split_list(out, [num_carry])
  out_ = iter(out)
  out = [next(out_) if f is None else _maybe_put(args_flat[f]) for f in ext_to_ext_fwd]
  assert next(out_, None) is None
  out = [*carry_out, *out]

  if any(move_to_const):
    out = pe.merge_lists(move_to_const + [False] * num_ys, out, new_consts)

  return out_avals.update(out).unflatten()


def scan(
    fn: Callable[..., Any],
    in_axes: Any,
    out_axes: Any,
    length: int | None = None,
    reverse: bool = False,
    unroll: int = 1,
    _split_transpose: bool = False,
    check_constancy_invariants: bool = True,
):
  """A wrapper around `jax.lax.scan` with in_axes/out_axes api.

  Example::
    def body_fn(b, c, x):
      return b + 2, c + 1, 2 * x

    loop = scan(body_fn, in_axes=0, out_axes=0)
    broadcast_in = 1
    carry = 2
    xs = jnp.arange(3)
    broadcast_out, carry, ys = loop(broadcast_in, carry, xs)
    print(broadcast_out)  # prints: 3
    print(carry)  # prints: 5
    print(ys)  # prints: [0, 2, 4]


  Args:
    fn: the body function of the scan loop of the form
      `(broadcast_in, carry, *args) -> (broadcast_out, carry, scan_out)`.
      the broadcast argument allows for loop independent inputs/outputs to
      be computed inside `fn`. `fn` will be called once to compute
      `broadcast_out`. The actual loop will receive `broadcast_out` as the new
      `broadcast_in`. This is useful for initializing values inside the loop.
    in_axes: specifies the axis along which arguments are scanned.
      Use `broadcast` to use the same value across iterations.
    out_axes: specifies the axis along which outputs are concatenated.
      Use `broadcast` if a return value should not be concatenated and
      is independent of the loop body.
    length: number of iterations. Only needs to be specified if there
      is no scan axis from which it can be derived.
    reverse: scan in reverse order from end to start.
    unroll: how many scan iterations to unroll within a single
      iteration of a loop (default: 1).
    _split_transpose: An experimental feature to split the transpose of scan
       into a scan and a map, backed by an experimental Jax lax.scan() feature.
    check_constancy_invariants: If true, the scan will verify that the
      broadcast constants are true loop invariants, and further supports
      broadcast function (non-carry) outputs.  This requires an extra jax
      tracing step however, so setting to false can reduce trace time on larger
      models.
  Returns:
     the function that performs the scan of the form:
     (broadcast_in, carry_in, *args) -> (broadcast_out, carry_out, scan_out).
  """

  def transpose_to_front(ax, xs):
    if ax is broadcast:
      return ()
    if ax == 0:
      return xs

    def trans(x):
      perm = tuple(range(x.ndim))
      perm = (ax,) + tuple(np.delete(perm, ax))
      return jnp.transpose(x, perm)

    return jax.tree_util.tree_map(trans, xs)

  def transpose_from_front(ax, xs):
    if ax is broadcast:
      return ()
    if ax == 0:
      return xs

    def trans(x):
      if ax < 0:
        pax = x.ndim + ax
      else:
        pax = ax
      assert pax < x.ndim
      perm = tuple(range(1, pax + 1)) + (0,) + tuple(range(pax + 1, x.ndim))
      return jnp.transpose(x, perm)

    return jax.tree_util.tree_map(trans, xs)

  def scan_fn(broadcast_in, init, *args):
    # Requires one extra tracing operation to test invariants:
    # Verifies that broadcast constants are true loop invariants, and further
    # supports broadcast function (non-carry) outputs.

    xs = jax.tree_util.tree_map(transpose_to_front, in_axes, args)

    def body_fn(c, xs, init_mode=False):
      # inject constants
      xs = jax.tree_util.tree_map(
          lambda ax, arg, x: (arg if ax is broadcast else x), in_axes, args, xs
      )
      broadcast_out, c, ys = fn(broadcast_in, c, *xs)

      if init_mode:
        ys = jax.tree_util.tree_map(
            lambda ax, y: (y if ax is broadcast else ()), out_axes, ys
        )
        return broadcast_out, ys
      else:
        ys = jax.tree_util.tree_map(
            lambda ax, y: (() if ax is broadcast else y), out_axes, ys
        )
        return c, ys

    broadcast_body = functools.partial(body_fn, init_mode=True)

    init_flat, carry_tree = jax.tree.flatten(init)
    xs_flat, scan_tree = jax.tree.flatten(xs)
    carry_avals = [build_shaped_array(x) for x in init_flat]
    scan_avals = [build_shaped_array(x, batch_dim=True) for x in  xs_flat]
    in_avals = [*carry_avals, *scan_avals]
    in_tree = jax.tree_util.treedef_tuple((carry_tree, scan_tree))
    assert all(isinstance(a, core.AbstractValue) for a in in_avals), in_avals

    debug_info = jax.api_util.debug_info("flax scan", broadcast_body,
                                         (in_tree,), {})
    f_flat, out_tree = jax.api_util.flatten_fun_nokwargs(
        lu.wrap_init(broadcast_body, debug_info=debug_info), in_tree
    )
    in_pvals = list(map(pe.PartialVal.unknown, in_avals))
    _, out_pvals, _ = pe.trace_to_jaxpr_nounits(f_flat, in_pvals)

    out_flat = []
    for pv, const in out_pvals:
      if pv is not None:
        raise ValueError(
            'broadcasted variable has a data dependency on the scan body.'
        )
      out_flat.append(const)
    broadcast_in, constants_out = jax.tree_util.tree_unflatten(
        out_tree(), out_flat
    )

    if jax.version.__version_info__ > (0, 4, 25):
      c, ys = lax.scan(
          body_fn, init, xs, length=length, reverse=reverse, unroll=unroll,
          _split_transpose=_split_transpose
      )
    else:
      c, ys = lax.scan(
          body_fn, init, xs, length=length, reverse=reverse, unroll=unroll
      )
    ys = jax.tree_util.tree_map(transpose_from_front, out_axes, ys)
    ys = jax.tree_util.tree_map(
        lambda ax, const, y: (const if ax is broadcast else y),
        out_axes,
        constants_out,
        ys,
    )
    return broadcast_in, c, ys

  def simple_scan_fn(broadcast_in, init, *args):
    # Saves an extra tracing operation.
    # No verification of constancy, and no support for non-carry broadcast
    # function outputs.
    xs = jax.tree_util.tree_map(transpose_to_front, in_axes, args)

    if broadcast in jax.tree_util.tree_leaves(out_axes):
      raise ValueError(f"nn.scan run with check_constancy_invariants=False "
                       f"does not support broadcast non-carry function "
                       f"outputs.  out_axes was given as {out_axes}")

    def body_fn(c, xs):
      # inject constants
      xs = jax.tree_util.tree_map(
          lambda ax, arg, x: (arg if ax is broadcast else x), in_axes, args, xs
      )
      _, c, ys = fn(broadcast_in, c, *xs)
      return c, ys

    if jax.version.__version_info__ > (0, 4, 25):
      c, ys = lax.scan(
          body_fn, init, xs, length=length, reverse=reverse, unroll=unroll,
          _split_transpose=_split_transpose
      )
    else:
      c, ys = lax.scan(
          body_fn, init, xs, length=length, reverse=reverse, unroll=unroll
      )
    ys = jax.tree_util.tree_map(transpose_from_front, out_axes, ys)
    return broadcast_in, c, ys

  if check_constancy_invariants:
    return scan_fn
  else:
    return simple_scan_fn


def scan(
  fn: Callable[..., Any],
  variable_axes: Mapping[CollectionFilter, InOutScanAxis] = {},
  variable_broadcast: CollectionFilter = False,
  variable_carry: CollectionFilter = False,
  split_rngs: Mapping[PRNGSequenceFilter, bool] = {},
  in_axes=0,
  out_axes=0,
  length: int | None = None,
  reverse: bool = False,
  unroll: int = 1,
  _split_transpose: bool = False,
  data_transform: Callable[..., Any] | None = None,
  metadata_params: dict[Any, Any] = {},
  check_constancy_invariants: bool = True,
) -> Callable[..., Any]:
  """A lifted version of ``jax.lax.scan``.

  See ``jax.lax.scan`` for the unlifted scan in Jax.

  To improve consistency with ``vmap``, this version of scan
  uses ``in_axes`` and ``out_axes`` to determine which arguments
  are scanned over and along which axis.

  ``scan`` distinguishes between 3 different types of values inside the loop:

  1. **scan**: a value that is iterated over in a loop. All scan values must
    have the same size in the axis they are scanned over. Scanned outputs
    will be stacked along the scan axis.
  2. **carry**: A carried value is updated at each loop iteration. It must
    have the same shape and dtype throughout the loop.
  3. **broadcast**: a value that is closed over by the loop. When a variable
    is broadcasted they are typically initialized inside the loop body but
    independent of the loop variables.

  The loop body should have the signature
  ``(scope, body, carry, *xs) -> (carry, ys)``, where ``xs`` and ``ys``
  are the scan values that go in and out of the loop.

  Example::

    scope.variable('counter', 'i', jnp.zeros, ())
    def body_fn(scope, c, x):
      counter = scope.variable('counter', 'i', jnp.zeros, ())
      counter.value += 1
      x = scope.child(nn.dense)(x, 1)
      return c, x

    _, ys = lift.scan(
        body_fn,
        variable_carry='counter',
        variable_broadcast='params',
        split_rngs={'params': False})(scope, (), xs)

  Args:
    fn: the function to be transformed.
    variable_axes: the variable collections that are scanned over.
    variable_broadcast: Specifies the broadcasted variable collections.
      A broadcasted variable should not depend on any computation that cannot b
      lifted out of the loop. This is typically used to define shared parameters
      inside the fn.
    variable_carry: Specifies the variable collections that are carried through
      the loop. Mutations to these variables are carried to the next iteration
      and will be preserved when the scan finishes.
    split_rngs: Split PRNG sequences will be different for each loop iterations.
      If split is False the PRNGs will be the same across iterations.
    in_axes: Specifies the axis to scan over for the arguments. Should be a
      prefix tree of the arguments. Use `flax.core.broadcast` to feed an entire
      input to each iteration of the scan body.
    out_axes: Specifies the axis to scan over for the return value. Should be a
      prefix tree of the return value.
    length: Specifies the number of loop iterations. This only needs
      to be specified if it cannot be derived from the scan arguments.
    reverse: If true, scan from end to start in reverse order.
    unroll: how many scan iterations to unroll within a single
      iteration of a loop (default: 1).
    _split_transpose: An experimental feature to split the transpose of a scan
       into a scan and a map, backed by an experimental Jax lax.scan() feature.
    data_transform: optional function to transform raw variable and rng groups,
      intended for inline SPMD annotations.
    metadata_params: arguments dict passed to AxisMetadata instances in the
      variable tree.
    check_constancy_invariants: If true, the scan will verify that the
      broadcast constants are true loop invariants, and further supports
      broadcast function (non-carry) outputs.  This requires an extra jax
      tracing step however, so setting to false can reduce trace time on larger
      models.

  Returns:
    The scan function with the signature
    ``(scope, carry, *xxs) -> (carry, yys)``, where ``xxs`` and ``yys`` are the
    scan values that go in and out of the loop.
  """
  variable_in_axes, variable_out_axes = _split_in_out_axes(variable_axes)
  variable_in_groups, variable_in_axes = _unzip2(variable_in_axes.items())
  variable_out_groups, variable_out_axes = _unzip2(variable_out_axes.items())
  assert all(isinstance(ax, int) for ax in variable_in_axes)
  assert all(isinstance(ax, int) for ax in variable_out_axes)
  rng_groups, rng_splits = _unzip2(split_rngs.items())
  rng_axes = tuple(
    0 if rng_split else axes_scan.broadcast for rng_split in rng_splits
  )

  def inner(scope_fn, repack_fn, variable_groups, rng_groups, init, *args):
    def find_length(axis, x):
      if axis is not axes_scan.broadcast:
        leaves = jax.tree_util.tree_leaves(x)
        if leaves:
          return leaves[0].shape[axis]
      return ()

    # split rngs
    lengths = jax.tree_util.tree_map(find_length, in_axes, args)
    lengths = set(jax.tree_util.tree_leaves(lengths))
    if length is None and len(lengths) == 1:
      (d_length,) = lengths
    elif len(lengths) > 1:
      raise ValueError(f'Inconsistent scan lengths: {lengths}')
    elif length is None:
      raise ValueError('length should be specified manually.')
    else:
      d_length = length
    # random.clone is only available on Jax versions 0.4.26 or newer
    # see: https://jax.readthedocs.io/en/latest/jax.experimental.key_reuse.html
    if hasattr(random, 'clone'):
      split_fn = lambda rng: random.split(random.clone(rng), d_length)
    else:
      split_fn = lambda rng: random.split(rng, d_length)

    rng_groups = tuple(
        tree_map_rngs(split_fn, rng_group) if split else rng_group
        for rng_group, split in zip(rng_groups, rng_splits)
    )

    @functools.partial(
        axes_scan.scan,
        in_axes=(variable_in_axes, rng_axes, in_axes),
        out_axes=(out_axes, variable_out_axes),
        length=length,
        reverse=reverse,
        unroll=unroll,
        _split_transpose=_split_transpose,
        check_constancy_invariants=check_constancy_invariants,
    )
    def scanned(broadcast_vars, carry, scan_variable_groups, rng_groups, args):
      carry_vars, c = carry
      variable_groups = (broadcast_vars, carry_vars) + scan_variable_groups
      if data_transform is not None:
        variable_groups, rng_groups = data_transform(
            variable_groups, rng_groups
        )
      scope = scope_fn(variable_groups, rng_groups)
      c, y = fn(scope, c, *args)
      out_vars = repack_fn(scope)
      broadcast_vars_out = out_vars[0]
      carry_vars = out_vars[1]
      scan_vars = out_vars[2:]
      # add immutable broadcast vars back to broadcast output
      # otherwise they won't be fed to the actual scan body
      for in_group, out_group in zip(broadcast_vars, broadcast_vars_out):
        for col in in_group:
          if col not in out_group:
            out_group[col] = in_group[col]
      return broadcast_vars_out, (carry_vars, c), (y, scan_vars)

    broadcast_vars = variable_groups[0]
    carry_vars = variable_groups[1]
    scan_vars = variable_groups[2:]
    new_scan_vars = []
    for scan_group, axis in zip(scan_vars, variable_in_axes):
      new_scan_vars.append(meta.remove_axis(scan_group, axis, metadata_params))
    broadcast_vars, (carry_vars, c), (ys, scan_vars) = scanned(
      broadcast_vars,
      (carry_vars, init),
      tuple(new_scan_vars),
      rng_groups,
      args,
    )
    new_scan_vars = []
    for scan_group, axis in zip(scan_vars, variable_out_axes):
      new_scan_vars.append(meta.add_axis(scan_group, axis, metadata_params))
    scan_vars = tuple(new_scan_vars)
    out_vars = (
      broadcast_vars,
      carry_vars,
    ) + scan_vars
    return (c, ys), out_vars

  return pack(
    inner,
    (variable_broadcast, variable_carry) + variable_in_groups,
    (variable_broadcast, variable_carry) + variable_out_groups,
    rng_groups,
    name='scan',
  )


def scan(
  target: Target,
  variable_axes: Mapping[CollectionFilter, InOutScanAxis] = FrozenDict(),
  variable_broadcast: CollectionFilter = False,
  variable_carry: CollectionFilter = False,
  split_rngs: Mapping[PRNGSequenceFilter, bool] = FrozenDict(),
  in_axes=0,
  out_axes=0,
  length: int | None = None,
  reverse: bool = False,
  unroll: int = 1,
  data_transform: Callable[..., Any] | None = None,
  metadata_params: Mapping[Any, Any] = {},
  methods=None,
  _split_transpose: bool = False,
  check_constancy_invariants: bool = True,
) -> Target:
  """A lifted version of ``jax.lax.scan``.

  See ``jax.lax.scan`` for the unlifted scan in Jax.

  To improve consistency with ``vmap``, this version of scan
  uses ``in_axes`` and ``out_axes`` to determine which arguments
  are scanned over and along which axis.

  ``scan`` distinguishes between 3 different types of values inside the loop:

  #. **scan**: a value that is iterated over in a loop. All scan values must
     have the same size in the axis they are scanned over. Scanned outputs
     will be stacked along the scan axis.

  #. **carry**: A carried value is updated at each loop iteration. It must
     have the same shape and dtype throughout the loop.

  #. **broadcast**: a value that is closed over by the loop. When a variable
     is broadcasted they are typically initialized inside the loop body but
     independent of the loop variables.

  The ``target`` should have the signature
  ``(module, carry, *xs) -> (carry, ys)``, where ``xs`` and ``ys``
  are the scan values that go in and out of the loop.

  Example::

    >>> import flax.linen as nn
    >>> import jax
    >>> import jax.numpy as jnp
    ...
    >>> class LSTM(nn.Module):
    ...   features: int
    ...
    ...   @nn.compact
    ...   def __call__(self, x):
    ...     ScanLSTM = nn.scan(
    ...       nn.LSTMCell, variable_broadcast="params",
    ...       split_rngs={"params": False}, in_axes=1, out_axes=1)
    ...
    ...     lstm = ScanLSTM(self.features)
    ...     input_shape =  x[:, 0].shape
    ...     carry = lstm.initialize_carry(jax.random.key(0), input_shape)
    ...     carry, x = lstm(carry, x)
    ...     return x
    ...
    >>> x = jnp.ones((4, 12, 7))
    >>> module = LSTM(features=32)
    >>> y, variables = module.init_with_output(jax.random.key(0), x)

  Note that when providing a function to ``nn.scan``, the scanning happens over
  all arguments starting from the third argument, as specified by ``in_axes``.
  The previous example could also be written using the functional form as::

    >>> class LSTM(nn.Module):
    ...   features: int
    ...
    ...   @nn.compact
    ...   def __call__(self, x):
    ...
    ...     cell = nn.LSTMCell(self.features)
    ...     def body_fn(cell, carry, x):
    ...       carry, y = cell(carry, x)
    ...       return carry, y
    ...     scan = nn.scan(
    ...       body_fn, variable_broadcast="params",
    ...       split_rngs={"params": False}, in_axes=1, out_axes=1)
    ...
    ...     input_shape =  x[:, 0].shape
    ...     carry = cell.initialize_carry(
    ...       jax.random.key(0), input_shape)
    ...     carry, x = scan(cell, carry, x)
    ...     return x
    ...
    >>> module = LSTM(features=32)
    >>> variables = module.init(jax.random.key(0), jnp.ones((4, 12, 7)))

  You can also use ``scan`` to reduce the compilation time of your JAX program
  by merging multiple layers into a single scan loop, you can do this when
  you have a sequence of identical layers that you want to apply iteratively
  to an input. For example::

    >>> class ResidualMLPBlock(nn.Module):
    ...   @nn.compact
    ...   def __call__(self, x, _):
    ...     h = nn.Dense(features=2)(x)
    ...     h = nn.relu(h)
    ...     return x + h, None
    ...
    >>> class ResidualMLP(nn.Module):
    ...   n_layers: int = 4
    ...
    ...   @nn.compact
    ...   def __call__(self, x):
    ...     ScanMLP = nn.scan(
    ...       ResidualMLPBlock, variable_axes={'params': 0},
    ...       variable_broadcast=False, split_rngs={'params': True},
    ...       length=self.n_layers)
    ...     x, _ = ScanMLP()(x, None)
    ...     return x
    ...
    >>> model = ResidualMLP(n_layers=4)
    >>> variables = model.init(jax.random.key(42), jnp.ones((1, 2)))

  To reduce both compilation and memory usage, you can use :func:`remat_scan`
  which will in addition checkpoint each layer in the scan loop.

  Args:
    target: a ``Module`` or a function taking a ``Module`` as its first
      argument.
    variable_axes: the variable collections that are scanned over.
    variable_broadcast: Specifies the broadcasted variable collections. A
      broadcasted variable should not depend on any computation that cannot be
      lifted out of the loop. This is typically used to define shared parameters
      inside the fn.
    variable_carry: Specifies the variable collections that are carried through
      the loop. Mutations to these variables are carried to the next iteration
      and will be preserved when the scan finishes.
    split_rngs: Split PRNG sequences will be different for each loop iterations.
      If split is False the PRNGs will be the same across iterations.
    in_axes: Specifies the axis to scan over for the arguments. Should be a
      prefix tree of the arguments. Use ``flax.core.broadcast`` to feed an entire
      input to each iteration of the scan body.
    out_axes: Specifies the axis to scan over for the return value. Should be a
      prefix tree of the return value.
    length: Specifies the number of loop iterations. This only needs to be
      specified if it cannot be derived from the scan arguments.
    reverse: If true, scan from end to start in reverse order.
    unroll: how many scan iterations to unroll within a single iteration of a
      loop (default: 1).
    data_transform: optional function to transform raw functional-core variable
      and rng groups inside lifted scan body_fn, intended for inline SPMD
      annotations.
    metadata_params: arguments dict passed to AxisMetadata instances in the
      variable tree.
    methods: If ``target`` is a ``Module``, the methods of ``Module`` to scan over.
    _split_transpose: An experimental feature to split the transpose of a scan
       into a scan and a map, backed by an experimental Jax lax.scan() feature.
    check_constancy_invariants: If true, the scan will verify that the
      broadcast constants are true loop invariants, and further supports
      broadcast function (non-carry) outputs.  This requires an extra jax
      tracing step however, so setting to false can reduce trace time on larger
      models.

  Returns:
    The scan function with the signature ``(module, carry, *xs) -> (carry,
    ys)``, where ``xs`` and ``ys`` are the scan values that go in and out of
    the loop.
  """
  return lift_transform(
    lift.scan,
    target,
    variable_axes=variable_axes,
    variable_broadcast=variable_broadcast,
    variable_carry=variable_carry,
    split_rngs=split_rngs,
    in_axes=in_axes,
    out_axes=out_axes,
    length=length,
    reverse=reverse,
    unroll=unroll,
    _split_transpose=_split_transpose,
    data_transform=data_transform,
    metadata_params=metadata_params,
    methods=methods,
    check_constancy_invariants=check_constancy_invariants,
  )


def scan(
  *,
  length: int | None = None,
  reverse: bool = False,
  unroll: int | bool = 1,
  _split_transpose: bool = False,
  # extended api
  in_axes: int | None | type[Carry] | tuple[tp.Any, ...] = (Carry, 0),
  out_axes: tp.Any = (Carry, 0),
  # nnx specific
  transform_metadata: tp.Mapping[str, tp.Any] = FrozenDict({}),
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> tp.Callable[[F], F]:
  ...


def scan(
  f: F,
  *,
  length: int | None = None,
  reverse: bool = False,
  unroll: int | bool = 1,
  _split_transpose: bool = False,
  # extended api
  in_axes: int | None | type[Carry] | tuple[tp.Any, ...] = (Carry, 0),
  out_axes: tp.Any = (Carry, 0),
  # nnx specific
  transform_metadata: tp.Mapping[str, tp.Any] = FrozenDict({}),
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> F:
  ...


def scan(
  f: F | type[Missing] = Missing,
  *,
  length: int | None = None,
  reverse: bool = False,
  unroll: int | bool = 1,
  _split_transpose: bool = False,
  # extended api
  in_axes: int | None | type[Carry] | tuple[tp.Any, ...] = (Carry, 0),
  out_axes: tp.Any = (Carry, 0),
  # nnx specific
  transform_metadata: tp.Mapping[str, tp.Any] = FrozenDict({}),
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> F | tp.Callable[[F], F]:
  """A Flax NNX transformation of `jax.lax.scan`_.

  Example::

    import jax
    from flax import nnx

    class Block(nnx.Module):
      def __init__(self, input_dim, features, *, rngs):
        self.linear = nnx.Linear(input_dim, features, rngs=rngs)
        self.dropout = nnx.Dropout(0.1, rngs=rngs)

      def __call__(self, x: jax.Array):
        x = self.linear(x)
        x = self.dropout(x)
        x = jax.nn.relu(x)
        return x

    class Model(nnx.Module):
      def __init__(self, num_layers, features, *, rngs):
        # In this model implementation we create
        # multiple blocks using vmap

        # As Block contains dropout op, we prefer
        # to split RNG into num_layers of RNGs
        # using @nnx.split_rngs decorator.
        # Next, nnx.vmap creates a vectorized version of Block.
        # in_axes and out_axes define vectorization axis
        # of the input splitted rngs and the output Block instance.
        # Both axes should be 0.
        @nnx.split_rngs(splits=num_layers)
        @nnx.vmap(in_axes=(0,), out_axes=0)
        def create_block(rngs: nnx.Rngs):
          return Block(features, features, rngs=rngs)

        self.blocks = create_block(rngs)
        self.num_layers = num_layers

      def __call__(self, x):
        # Forward pass method implementation

        # We use nnx.scan to apply sequentially the blocks
        # on the input, for example with num_layers=3
        # output = block[0](x)
        # output = block[1](output)
        # output = block[2](output)
        #
        # In `forward` function defined below:
        # - x represents the loop carry value
        # - model is the data to scan along the leading axis
        # nnx.scan args:
        # - in_axes marks the inputs: x is marked as carry
        # and the model is to scan along the axis 0
        # - out_axes marks the output as carry
        @nnx.scan(in_axes=(nnx.Carry, 0), out_axes=nnx.Carry)
        def forward(x, model):
          x = model(x)
          return x

        return forward(x, self.blocks)

      # Alternatively, we can also decorate `self.__call__` method
      # @nnx.scan(in_axes=(0, nnx.Carry), out_axes=nnx.Carry)
      # def __call__(self, x):
      #   return self.blocks(x)

    model = Model(2, 4, rngs=nnx.Rngs(0))
    _, params, _ = nnx.split(model, nnx.Param, ...)
    print(params)  # kernel of shape: (2, 4, 4)

    x = jnp.arange(5 * 4, dtype="float32").reshape((5, 4))
    y = model(x)
    print(y.shape)  # shape: (5, 4)

  Args:
    f: a Python function to be scanned
    length: optional integer specifying the number of loop iterations
    reverse: optional boolean specifying whether to run the scan iteration
      forward (the default) or in reverse
    unroll: optional positive int or bool specifying, in the underlying
      operation of the scan primitive, how many scan iterations to unroll
      within a single iteration of a loop.
    in_axes: integer, None, :class:`flax.nnx.Carry` or sequence of values specifying
      the kind of input args. Integer value would specify the axis of corresponding
      input data to scan along. :class:`flax.nnx.Carry` marks the input data as
      loop carry value. None marks the input data as auxiliary input.
    out_axes: integer, None, :class:`flax.nnx.Carry` or sequence of values specifying
      the kind of output args. See ``in_axes`` for details. Note that If ``in_axes``
      contains :class:`flax.nnx.Carry` then ``out_axes`` must also contain :class:`flax.nnx.Carry`.
    graph_updates: If ``True``, propagates updates on graph structure
      that happen inside the transform to the input graphs, has no
      effect when ``graph=False``. When ``False``, using ``StateAxes``
      is not supported.

  .. _jax.lax.scan: https://jax.readthedocs.io/en/latest/_autosummary/jax.lax.scan.html>
  """
  if f is Missing:
    return functools.partial(
        scan,
        length=length,
        reverse=reverse,
        unroll=unroll,
        _split_transpose=_split_transpose,
        in_axes=in_axes,
        out_axes=out_axes,
        transform_metadata=transform_metadata,
        graph=graph,
        graph_updates=graph_updates,
    )  # type: ignore[return-value]

  f_unbound, _, was_bound = _resolve_bound_callable(f)
  if was_bound:
    _raise_bound_method_error('scan')

  if graph is None:
    graph = graphlib.set_graph_mode.current_value()
  if graph_updates is None:
    graph_updates = graphlib.set_graph_updates.current_value()

  extract.check_prefix(in_axes, 'in_axes', 'scan', graph, graph_updates)
  extract.check_prefix(out_axes, 'out_axes', 'scan', graph, graph_updates)
  _check_out_axes(out_axes)

  if not graph or not graph_updates:
    return _simple_scan(
      f, f_unbound, graph=graph,
      in_axes=in_axes, out_axes=out_axes,
      length=length, reverse=reverse, unroll=unroll,
      _split_transpose=_split_transpose,
    )

  return _graph_updates_scan(
    f, f_unbound,
    in_axes=in_axes, out_axes=out_axes,
    length=length, reverse=reverse, unroll=unroll,
    _split_transpose=_split_transpose,
    transform_metadata=transform_metadata,
  )

