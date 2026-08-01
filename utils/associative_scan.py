
def associative_scan(
    combine_fn: Callable[[pytree.PyTree, pytree.PyTree], pytree.PyTree],
    xs: pytree.PyTree,
    dim: int,
    reverse: bool = False,
    combine_mode: str = "pointwise",
) -> torch.Tensor:
    r"""
    Performs an inclusive scan with an associative combine function.

    .. warning::

        ``torch.associative_scan`` is a prototype feature in PyTorch. It currently
        does not support autograd and you may run into miscompiles.
        Read more about feature classification at:
        https://pytorch.org/blog/pytorch-feature-classification-changes/#prototype

    This operator requires runtime code generation and so requires support for
    ``torch.compile``. Further, only CUDA device codegen is supported at the moment.

    Args:
        combine_fn (Callable): A binary callable with type ``(Tensor, Tensor) -> Tensor``,
            or if input is a pytree ``(pytree, pytree) -> pytree``.
            This function must be pure, i.e., no lifted arguments are supported at the moment,
            satisfy the associative property and have no side-effects.
        xs (torch.Tensor): The input tensor, or nested pytree of tensors.
            All inputs are expected to have the same shape.
        dim (int): the dimension to scan over
        reverse (bool): A boolean stating if the scan should be reversed with respect to ``dim``, default ``False``.
        combine_mode (str): A string indicating whether the ``combine_fn`` is ``pointwise`` or ``generic``, default ``pointwise``.
            If ``combine_mode=pointwise``, ``combine_fn`` must be pure, may only contain pointwise operations
            and ``xs`` must be CUDA tensors.
            In all other cases ``combine_mode=generic`` should be used.
            Note: ``combine_mode=pointwise`` is more efficient than ``combine_mode=generic``.


    Example::

        def add(x: torch.Tensor, y: torch.Tensor):
            return x + y


        cumsum = associative_scan(add, x, dim)

    """
    # TODO: Support lifted arguments in inductor for associative_scan
    # TODO: Support autograd for cases with lifted arguments for combine_mode=pointwise

    # The reason we flatten xs before calling into dynamo is that
    # we want to create a consistent input ordering for combine_fn
    # and we also want to the input ordering matches the output ordering.
    leaves_xs_orig, spec_xs = pytree.tree_flatten(xs)

    def _validate_input(cfn, lxs, d, r, cm):
        # Basic arguments check
        if not callable(cfn):
            raise ValueError(f"Combine_fn must be a callable, but got {cfn}")
        if not isinstance(d, int):
            raise ValueError("Dim must be an int, but got " + str(type(d)))
        if not isinstance(r, bool):
            raise RuntimeError("Reverse must be a bool, but got " + str(type(r)))
        if cm not in ["pointwise", "generic"]:
            raise ValueError(
                f"Combine_mode must either 'pointwise' or 'generic', but got {cm}"
            )
        if cm == "pointwise" and not all(l.device.type in ("cuda", "xpu") for l in lxs):
            raise ValueError(
                "For combine_mode='pointwise', all input tensors need to be on CUDA or XPU"
            )

        # Checks for xs
        if len(lxs) == 0:
            raise ValueError("Expected at least 1 xs leaf")
        if any(not isinstance(x, torch.Tensor) for x in lxs):
            raise ValueError("xs leaves must be a Tensor")
        if any(x.is_sparse for x in lxs):
            raise ValueError(
                "xs leaves must dense Tensors, consider using `to_dense()`"
            )
        if any(x.ndim <= d for x in lxs):
            raise ValueError(
                "All xs leaves must at least have 'dim' number of dimensions and scan dimension > 0"
            )
        if any(x.shape[d] == 0 for x in lxs):
            raise ValueError(
                "All xs leaves must at least have 'dim' number of dimensions and scan dimension > 0"
            )

    ndim = leaves_xs_orig[0].ndim
    dim = utils.canonicalize_dim(ndim, dim)

    _validate_input(combine_fn, leaves_xs_orig, dim, reverse, combine_mode)

    # Move scan dim to 0 and always perform scan on dim 0
    leaves_xs = [torch.movedim(elem, dim, 0) for elem in leaves_xs_orig]

    if reverse:
        leaves_xs = [torch.flip(elem, [0]) for elem in leaves_xs]

    if combine_mode == "generic":
        # The generic_associative_scan implementation calls the combine_fn with a `batch` along the scan dimension
        # For example, consider:
        # def add(x: torch.Tensor, y: torch.Tensor):
        #     return x + y
        # leaves = torch.tensor([[0.0, 1.0, 2.0, 3.0]
        #                        [0.0, 1.0, 2.0, 3.0]])
        # which has shape 2 x 4;
        # dim = 1;
        # In the first iteration of `_scan` the combine_fn gets invoked with
        # combine_fn([torch.tensor([[0.0, 2.0],
        #                           [0.0, 2.0]])],
        #            [torch.tensor([[1.0, 3.0],
        #                           [1.0, 3.0]])])
        # The arguments are of shape 2 x 2, but can be evaluated in parallel along the scan dimension.
        combine_fn = functools.partial(
            wrap_combine_fn_flat,
            combine_fn=torch.vmap(
                combine_fn,
                in_dims=(
                    pytree.tree_unflatten([0] * len(leaves_xs), spec_xs),
                    pytree.tree_unflatten([0] * len(leaves_xs), spec_xs),
                ),
                out_dims=0,
            ),
            spec=spec_xs,
            num_leaves=len(leaves_xs),
        )
        out = generic_associative_scan(combine_fn, leaves_xs, additional_inputs=())
        out = pytree.tree_unflatten(out, spec_xs)
    else:
        combine_fn = functools.partial(
            wrap_combine_fn_flat,
            combine_fn=combine_fn,
            spec=spec_xs,
            num_leaves=len(leaves_xs),
        )

        def run_flattened_associative_scan(combine_fn, leaves_xs):
            return associative_scan_op(combine_fn, leaves_xs, additional_inputs=())

        out = _maybe_compile_and_run_fn(
            run_flattened_associative_scan,
            combine_fn,
            leaves_xs,
        )

    if reverse:
        out = pytree.tree_map(lambda elem: elem.flip([0]), out)

    out = pytree.tree_map(lambda elem: torch.movedim(elem, 0, dim), out)

    return out


def associative_scan(
    combine_fn: ir.Subgraph, xs, additional_inputs: tuple[torch.Tensor]
):
    from .subgraph_lowering import InputDescriptor, lower_pointwise_subgraph

    if len(additional_inputs) > 0:
        raise RuntimeError(
            "Unable to generate code for associative_scan op, because there are lifted arguments"
        )

    subgraph_inputs = [
        InputDescriptor(dtype=x.get_dtype(), device=x.get_device())
        for x in itertools.chain(xs, xs)
    ]
    lowered_combine_fn = lower_pointwise_subgraph(combine_fn, subgraph_inputs)  # type: ignore[var-annotated]

    def wrapped_combine_fn(lhs, rhs):
        return lowered_combine_fn(
            *pytree.tree_leaves(lhs),
            *pytree.tree_leaves(rhs),
        )

    kwargs = _make_scan_inner(xs[0], axis=0, dtype=None)
    kwargs["dtypes"] = tuple(x.get_dtype() for x in xs)
    kwargs["inner_fns"] = tuple(x.make_loader() for x in xs)
    result = ir.Scan.create(
        combine_fn=wrapped_combine_fn,
        can_fallback_to_aten=False,
        **kwargs,
    )
    if result[0] is None:
        raise RuntimeError("Unable to generate code for associative_scan op")
    return result


def associative_scan(fn: Callable, elems, reverse: bool = False, axis: int = 0):
  """Performs a scan with an associative binary operation, in parallel.

  For an introduction to associative scans, see [BLE1990]_.

  Args:
    fn: A Python callable implementing an associative binary operation with
      signature ``r = fn(a, b)``. Function `fn` must be associative, i.e., it
      must satisfy the equation
      ``fn(a, fn(b, c)) == fn(fn(a, b), c)``.

      The inputs and result are (possibly nested Python tree structures of)
      array(s) matching ``elems``. Each array has a dimension in place
      of the ``axis`` dimension. `fn` should be applied elementwise over
      the ``axis`` dimension (for example, by using :func:`jax.vmap` over the
      elementwise function.)

      The result ``r`` has the same shape (and structure) as the two inputs
      ``a`` and ``b``.
    elems: A (possibly nested Python tree structure of) array(s), each with
      an ``axis`` dimension of size ``num_elems``.
    reverse: A boolean stating if the scan should be reversed with respect to
      the ``axis`` dimension.
    axis: an integer identifying the axis over which the scan should occur.

  Returns:
    A (possibly nested Python tree structure of) array(s) of the same shape
    and structure as ``elems``, in which the ``k``'th element of ``axis`` is the
    result of recursively applying ``fn`` to combine the first ``k`` elements
    of ``elems`` along ``axis``. For example, given ``elems = [a, b, c, ...]``,
    the result would be ``[a, fn(a, b), fn(fn(a, b), c), ...]``.

    If ``elems = [..., x, y, z]`` and ``reverse`` is true, the result is
    ``[..., f(f(z, y), x), f(z, y), z]``.

  Example 1: partial sums of an array of numbers:

  >>> lax.associative_scan(jnp.add, jnp.arange(0, 4))
  Array([0, 1, 3, 6], dtype=int32)

  Example 2: partial products of an array of matrices

  >>> mats = jax.random.uniform(jax.random.key(0), (4, 2, 2))
  >>> partial_prods = lax.associative_scan(jnp.matmul, mats)
  >>> partial_prods.shape
  (4, 2, 2)

  Example 3: reversed partial sums of an array of numbers

  >>> lax.associative_scan(jnp.add, jnp.arange(0, 4), reverse=True)
  Array([6, 6, 5, 3], dtype=int32)

  .. [BLE1990] Blelloch, Guy E. 1990. "Prefix Sums and Their Applications.",
    Technical Report CMU-CS-90-190, School of Computer Science, Carnegie Mellon
    University.
  """
  if not callable(fn):
    raise TypeError("lax.associative_scan: fn argument should be callable.")
  elems_flat, tree = tree_flatten(elems)

  if reverse:
    elems_flat = [lax.rev(elem, [axis]) for elem in elems_flat]

  def combine(a_flat, b_flat):
    # Lower `fn` to operate on flattened sequences of elems.
    a = tree_unflatten(tree, a_flat)
    b = tree_unflatten(tree, b_flat)
    c = fn(a, b)
    c_flat, _ = tree_flatten(c)
    return c_flat

  # Check that all inputs have a consistent leading dimension `num_elems`.
  axis = util.canonicalize_axis(axis, elems_flat[0].ndim)

  if not core.is_constant_dim(elems_flat[0].shape[axis]):
    raise NotImplementedError("associative scan over axis "
        f"of non-constant size: {elems_flat[0].shape[axis]}. You may be "
        "able to avoid this on TPU. See b/274176030.")
  num_elems = int(elems_flat[0].shape[axis])
  if not all(int(elem.shape[axis]) == num_elems for elem in elems_flat[1:]):
    raise ValueError('Array inputs to associative_scan must have the same '
                     'first dimension. (saw: {})'
                     .format([elem.shape for elem in elems_flat]))


  # Summary of algorithm:
  #
  # Consider elements of `_scan(elems)` at odd indices. That's the same as first
  # summing successive pairs of elements of `elems` and performing a scan on
  # that half sized tensor. We perform the latter scan by recursion.
  #
  # Now consider the even elements of `_scan(elems)`. These can be computed
  # from the odd elements of `_scan(elems)` by adding each odd element of
  # `_scan(elems)` to the matching even element in the original `elems`.
  #
  # We return the odd and even elements interleaved.
  #
  # For the base case of the recursion we return the first element
  # of `elems` followed by the sum of the first two elements computed as
  # a (small two-down-to-one) reduction step.
  def _scan(elems):
    """Perform scan on `elems`."""

    num_elems = elems[0].shape[axis]

    if num_elems < 2:
      return elems

    # Combine adjacent pairs of elements.
    reduced_elems = combine(
      [slicing.slice_in_dim(elem, 0, -1, stride=2, axis=axis) for elem in elems],
      [slicing.slice_in_dim(elem, 1, None, stride=2, axis=axis)
       for elem in elems])

    # Recursively compute scan for partially reduced tensors.
    odd_elems = _scan(reduced_elems)

    if num_elems % 2 == 0:
      even_elems = combine(
        [slicing.slice_in_dim(e, 0, -1, axis=axis) for e in odd_elems],
        [slicing.slice_in_dim(e, 2, None, stride=2, axis=axis) for e in elems])
    else:
      even_elems = combine(
        odd_elems,
        [slicing.slice_in_dim(e, 2, None, stride=2, axis=axis) for e in elems])

    # The first element of a scan is the same as the first element
    # of the original `elems`.
    even_elems = [
      lax.concatenate([slicing.slice_in_dim(elem, 0, 1, axis=axis), result],
                      dimension=axis)
      for (elem, result) in zip(elems, even_elems)]
    return list(_map(partial(_interleave, axis=axis), even_elems, odd_elems))

  scans = _scan(elems_flat)

  if reverse:
    scans = [lax.rev(scanned, [axis]) for scanned in scans]

  return tree_unflatten(tree, scans)

