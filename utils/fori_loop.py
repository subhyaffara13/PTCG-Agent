
def fori_loop(lower, upper, body_fun, init_val,
              *, unroll: int | bool | None = None):
  """Loop from ``lower`` to ``upper`` by reduction to :func:`jax.lax.while_loop`.

  The `Haskell-like type signature`_ in brief is

  .. code-block:: haskell

    fori_loop :: Int -> Int -> ((Int, a) -> a) -> a -> a

  The semantics of ``fori_loop`` are given by this Python implementation::

    def fori_loop(lower, upper, body_fun, init_val):
      val = init_val
      for i in range(lower, upper):
        val = body_fun(i, val)
      return val

  As the Python version suggests, setting ``upper <= lower`` will produce no
  iterations. Negative or custom increments are not supported.

  Unlike that Python version, ``fori_loop`` is implemented in terms of either a
  call to :func:`jax.lax.while_loop` or a call to :func:`jax.lax.scan`. If the
  trip count is static (meaning known at tracing time, perhaps because ``lower``
  and ``upper`` are Python integer literals) then the ``fori_loop`` is
  implemented in terms of :func:`~scan` and reverse-mode autodiff is supported;
  otherwise, a ``while_loop`` is used and reverse-mode autodiff is not
  supported.  See those functions' docstrings for more information.

  Also unlike the Python analogue, the loop-carried value ``val`` must hold a
  fixed shape and dtype across all iterations (and not just be consistent up to
  NumPy rank/shape broadcasting and dtype promotion rules, for example). In
  other words, the type ``a`` in the type signature above represents an array
  with a fixed shape and dtype (or a nested tuple/list/dict container data
  structure with a fixed structure and arrays with fixed shape and dtype at the
  leaves).

  .. note::
    :py:func:`fori_loop` compiles ``body_fun``, so while it can be combined with
    :py:func:`jit`, it's usually unnecessary.

  Args:
    lower: an integer representing the loop index lower bound (inclusive)
    upper: an integer representing the loop index upper bound (exclusive)
    body_fun: function of type ``(int, a) -> a``.
    init_val: initial loop carry value of type ``a``.
    unroll: An optional integer or boolean that determines how much to unroll
      the loop. If an integer is provided, it determines how many unrolled
      loop iterations to run within a single rolled iteration of the loop. If a
      boolean is provided, it will determine if the loop is completely unrolled
      (i.e. `unroll=True`) or left completely unrolled (i.e. `unroll=False`).
      This argument is only applicable if the loop bounds are statically known.

  Returns:
    Loop value from the final iteration, of type ``a``.

  .. _Haskell-like type signature: https://wiki.haskell.org/Type_signature
  """
  if not callable(body_fun):
    raise TypeError("lax.fori_loop: body_fun argument should be callable.")

  # TODO(phawkins): perhaps do more type checking here, better error messages.
  lower_dtype = lax.dtype(lower)
  upper_dtype = lax.dtype(upper)
  if lower_dtype == upper_dtype:
    dtype = lower_dtype
  else:
    # As a special case: allow promotion of weak integers (e.g., Python scalars)
    # This improves the ergonomics if one but not both of the loop bounds is a
    # scalar.
    dtype = None
    if (np.issubdtype(lower_dtype, np.signedinteger) and
        np.issubdtype(upper_dtype, np.signedinteger)):
      lower_weak = dtypes.is_weakly_typed(lower)
      upper_weak = dtypes.is_weakly_typed(upper)
      if lower_weak and not upper_weak:
        dtype = upper_dtype
      elif not lower_weak and upper_weak:
        dtype = lower_dtype

    if dtype is None:
      raise TypeError("lower and upper arguments to fori_loop must have equal "
                      f"types, got {lower_dtype.name} and {upper_dtype.name}")

  # If we can specialize on the trip count, call scan instead of a while_loop
  # to enable efficient reverse-mode differentiation.
  lower_ = upper_ = 0
  if core.is_concrete(lower) and core.is_concrete(upper):
    try:
      lower_ = int(lower)
      upper_ = int(upper)
    except (TypeError, core.InconclusiveDimensionOperation):
      use_scan = False
    else:
      use_scan = True
  else:
    use_scan = False

  body_fun_dbg = api_util.debug_info("fori_loop", body_fun,
                                     (0, init_val), {})

  if use_scan:
    if unroll is None:
      unroll = False
    length = max(upper_ - lower_, 0)
    if config.disable_jit.value and length == 0:
      # non-jit implementation of scan does not support length=0
      return init_val
    scan_body = _fori_scan_body_fun(body_fun, body_fun_dbg)
    (_, result), _ = scan(
        scan_body,
        (lower_, init_val),
        None,
        length=length,
        unroll=unroll,
    )
    return result
  if unroll is not None and unroll is not False and unroll != 1:
    raise ValueError("Can only use `unroll` in `fori_loop` if the loop bounds "
                     "are statically known.")

  if lower_dtype != dtype:
    lower = lax.convert_element_type(lower, dtype)
  if upper_dtype != dtype:
    upper = lax.convert_element_type(upper, dtype)
  while_body_fun = _fori_body_fun(body_fun, body_fun_dbg)
  _, _, result = while_loop(_fori_cond_fun, while_body_fun,
                            (lower, upper, init_val))
  return result


def fori_loop(lower: int, upper: int,
              body_fun: tp.Callable[[int, T], T],
              init_val: T,
              *,
              unroll: int | bool | None = None,
              graph: bool | None = None,
              graph_updates: bool | None = None) -> T:
  """A Flax NNX transformation of `jax.lax.fori_loop <https://jax.readthedocs.io/en/latest/_autosummary/jax.lax.fori_loop.html>`_.

  Caution: for the NNX internal reference tracing mechanism to work, you cannot
  change the variable reference structure of `init_val` inside `body_fun`.

  Example::

    >>> import jax
    >>> from flax import nnx

    >>> def fwd_fn(i, input):
    ...   m, x = input
    ...   m.kernel[...] = jnp.identity(10) * i
    ...   return m, m(x)

    >>> module = nnx.Linear(10, 10, rngs=nnx.Rngs(0))
    >>> x = jax.random.normal(jax.random.key(0), (10,))
    >>> _, y = nnx.fori_loop(2, 4, fwd_fn, (module, x))
    >>> np.testing.assert_array_equal(y, x * 2 * 3)


  Args:
    lower: An integer representing the loop index lower bound (inclusive).
    upper: An integer representing the loop index upper bound (exclusive).
    body_fun: a function that takes an input of type ``T`` and outputs an ``T``.
      Note that both data and modules of ``T`` must have the same reference
      structure between inputs and outputs.
    init_val: the initial input for body_fun. Must be of type ``T``.
    unroll: An optional integer or boolean that determines how much to unroll
      the loop. If an integer is provided, it determines how many unrolled
      loop iterations to run within a single rolled iteration of the loop. If a
      boolean is provided, it will determine if the loop is competely unrolled
      (i.e. ``unroll=True``) or left completely unrolled (i.e. ``unroll=False``).
      This argument is only applicable if the loop bounds are statically known.
    graph: if True, use graph-mode (default). If False, use tree-mode.
      If None, uses the value of ``nnx_graph_mode`` config.
    graph_updates: If ``True``, propagates updates on graph structure
      that happen inside the transform to the input graphs, has no
      effect when ``graph=False``.

  Returns:
    A loop value from the final iteration, of type ``T``.

  """
  if graph is None:
    graph = graphlib.set_graph_mode.current_value()
  if graph_updates is None:
    graph_updates = graphlib.set_graph_updates.current_value()
  if not graph or not graph_updates:
    simple_body_fn = SimpleForiLoopBodyFn(body_fun, graph=graph)

    if graph:
      init_val = extract.to_tree2(init_val)
    val_out = jax.lax.fori_loop(
      lower, upper,
      simple_body_fn,
      init_val,
      unroll=unroll,
    )
    val_out = extract.update_carry_variables(init_val, val_out)
    if graph:
      val_out = extract.from_tree2(val_out)
    return val_out

  pure_init_val = extract.to_tree(init_val, ctxtag='fori_loop')
  body = ForiLoopBodyFn(body_fun)
  pure_out = jax.eval_shape(body, lower, pure_init_val)
  pure_init_val = _reconsile_index_mapping(pure_init_val, pure_out)
  pure_out = jax.lax.fori_loop(lower, upper,
                               body, pure_init_val,
                               unroll=unroll)
  out = extract.from_tree(pure_out, ctxtag='fori_loop', is_inner=False)
  return out

