import functools
import random
from typing import Any, Callable

def vmap(func: Callable, in_dims: in_dims_t = 0, out_dims: out_dims_t = 0) -> Callable:
    """
    Please use torch.vmap instead of this API.
    """
    return _vmap(func, in_dims, out_dims)


def vmap(
    func: Callable[_P, _R],
    in_dims: in_dims_t = 0,
    out_dims: out_dims_t = 0,
    randomness: str = "error",
    *,
    chunk_size: int | None = None,
) -> Callable[_P, _R]:
    """
    vmap is the vectorizing map; ``vmap(func)`` returns a new function that
    maps ``func`` over some dimension of the inputs. Semantically, vmap
    pushes the map into PyTorch operations called by ``func``, effectively
    vectorizing those operations.

    vmap is useful for handling batch dimensions: one can write a function
    ``func`` that runs on examples and then lift it to a function that can
    take batches of examples with ``vmap(func)``. vmap can also be used to
    compute batched gradients when composed with autograd.

    .. note::
        :func:`torch.vmap` is aliased to :func:`torch.func.vmap` for
        convenience. Use whichever one you'd like.

    Args:
        func (function): A Python function that takes one or more arguments.
            Must return one or more Tensors.
        in_dims (int or nested structure): Specifies which dimension of the
            inputs should be mapped over. ``in_dims`` should have a
            structure like the inputs. If the ``in_dim`` for a particular
            input is None, then that indicates there is no map dimension.
            Default: 0.
        out_dims (int or Tuple[int]): Specifies where the mapped dimension
            should appear in the outputs. If ``out_dims`` is a Tuple, then
            it should have one element per output. Default: 0.
        randomness (str): Specifies whether the randomness in this
            vmap should be the same or different across batches. If 'different',
            the randomness for each batch will be different. If 'same', the
            randomness will be the same across batches. If 'error', any calls to
            random functions will error. Default: 'error'. WARNING: this flag
            only applies to random PyTorch operations and does not apply to
            Python's random module or numpy randomness.
        chunk_size (None or int): If None (default), apply a single vmap over inputs.
            If not None, then compute the vmap :attr:`chunk_size` samples at a time.
            Note that :attr:`chunk_size=1` is equivalent to computing the vmap with a for-loop.
            If you run into memory issues computing the vmap, please try a non-None chunk_size.

    Returns:
        Returns a new "batched" function. It takes the same inputs as
        ``func``, except each input has an extra dimension at the index
        specified by ``in_dims``. It takes returns the same outputs as
        ``func``, except each output has an extra dimension at the index
        specified by ``out_dims``.

    .. warning:
        :func:`vmap` works best with functional-style code. Please do not
        perform any side-effects in ``func``, with the exception of
        in-place PyTorch operations. Examples of side-effects include mutating
        Python data structures and assigning values to variables not captured
        in ``func``.

    One example of using :func:`vmap` is to compute batched dot products. PyTorch
    doesn't provide a batched ``torch.dot`` API; instead of unsuccessfully
    rummaging through docs, use :func:`vmap` to construct a new function.

        >>> torch.dot  # [D], [D] -> []
        >>> batched_dot = torch.func.vmap(torch.dot)  # [N, D], [N, D] -> [N]
        >>> x, y = torch.randn(2, 5), torch.randn(2, 5)
        >>> batched_dot(x, y)

    :func:`vmap` can be helpful in hiding batch dimensions, leading to a simpler
    model authoring experience.

        >>> batch_size, feature_size = 3, 5
        >>> weights = torch.randn(feature_size, requires_grad=True)
        >>>
        >>> def model(feature_vec):
        >>> # Very simple linear model with activation
        >>>     return feature_vec.dot(weights).relu()
        >>>
        >>> examples = torch.randn(batch_size, feature_size)
        >>> result = torch.vmap(model)(examples)

    :func:`vmap` can also help vectorize computations that were previously difficult
    or impossible to batch. One example is higher-order gradient computation.
    The PyTorch autograd engine computes vjps (vector-Jacobian products).
    Computing a full Jacobian matrix for some function f: R^N -> R^N usually
    requires N calls to ``autograd.grad``, one per Jacobian row. Using :func:`vmap`,
    we can vectorize the whole computation, computing the Jacobian in a single
    call to ``autograd.grad``.

        >>> # Setup
        >>> N = 5
        >>> f = lambda x: x**2
        >>> x = torch.randn(N, requires_grad=True)
        >>> y = f(x)
        >>> I_N = torch.eye(N)
        >>>
        >>> # Sequential approach
        >>> jacobian_rows = [torch.autograd.grad(y, x, v, retain_graph=True)[0]
        >>>                  for v in I_N.unbind()]
        >>> jacobian = torch.stack(jacobian_rows)
        >>>
        >>> # vectorized gradient computation
        >>> def get_vjp(v):
        >>>     return torch.autograd.grad(y, x, v)
        >>> jacobian = torch.vmap(get_vjp)(I_N)

    :func:`vmap` can also be nested, producing an output with multiple batched dimensions

        >>> torch.dot  # [D], [D] -> []
        >>> batched_dot = torch.vmap(
        ...     torch.vmap(torch.dot)
        ... )  # [N1, N0, D], [N1, N0, D] -> [N1, N0]
        >>> x, y = torch.randn(2, 3, 5), torch.randn(2, 3, 5)
        >>> batched_dot(x, y)  # tensor of size [2, 3]

    If the inputs are not batched along the first dimension, ``in_dims`` specifies
    the dimension that each inputs are batched along as

        >>> torch.dot  # [N], [N] -> []
        >>> batched_dot = torch.vmap(torch.dot, in_dims=1)  # [N, D], [N, D] -> [D]
        >>> x, y = torch.randn(2, 5), torch.randn(2, 5)
        >>> batched_dot(
        ...     x, y
        ... )  # output is [5] instead of [2] if batched along the 0th dimension

    If there are multiple inputs each of which is batched along different dimensions,
    ``in_dims`` must be a tuple with the batch dimension for each input as

        >>> torch.dot  # [D], [D] -> []
        >>> batched_dot = torch.vmap(torch.dot, in_dims=(0, None))  # [N, D], [D] -> [N]
        >>> x, y = torch.randn(2, 5), torch.randn(5)
        >>> batched_dot(
        ...     x, y
        ... )  # second arg doesn't have a batch dim because in_dim[1] was None

    If the input is a Python struct, ``in_dims`` must be a tuple containing a struct
    matching the shape of the input:

        >>> f = lambda dict: torch.dot(dict["x"], dict["y"])
        >>> x, y = torch.randn(2, 5), torch.randn(5)
        >>> input = {"x": x, "y": y}
        >>> batched_dot = torch.vmap(f, in_dims=({"x": 0, "y": None},))
        >>> batched_dot(input)

    By default, the output is batched along the first dimension. However, it can be batched
    along any dimension by using ``out_dims``

        >>> f = lambda x: x**2
        >>> x = torch.randn(2, 5)
        >>> batched_pow = torch.vmap(f, out_dims=1)
        >>> batched_pow(x)  # [5, 2]

    For any function that uses kwargs, the returned function will not batch the kwargs but will
    accept kwargs

        >>> x = torch.randn([2, 5])
        >>> def fn(x, scale=4.):
        >>>   return x * scale
        >>>
        >>> batched_pow = torch.vmap(fn)
        >>> assert torch.allclose(batched_pow(x), x * 4)
        >>> batched_pow(x, scale=x)  # scale is not batched, output has shape [2, 2, 5]

    .. note::
        vmap does not provide general autobatching or handle variable-length
        sequences out of the box.
    """
    from torch.compiler import is_compiling

    _check_randomness_arg(randomness)
    if not (chunk_size is None or chunk_size > 0):
        raise ValueError(
            f"vmap: chunk_size should be None or greater than 0. (got {chunk_size})"
        )

    def wrapped(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        # pyrefly: ignore[bad-argument-type]
        return vmap_impl(
            # pyrefly: ignore[bad-argument-type]
            func,
            in_dims,
            out_dims,
            randomness,
            chunk_size,
            *args,
            **kwargs,
        )

    if not is_compiling():
        wrapped = functools.wraps(func)(wrapped)

    return wrapped


def vmap(
    func: Callable[..., Any],
    in_dims: in_dims_t = 0,
    out_dims: out_dims_t = 0,
    randomness: str = "error",
    *,
    chunk_size: int | None = None,
) -> Callable[..., Any]:
    warn_deprecated("vmap", "torch.vmap")
    return apis.vmap(func, in_dims, out_dims, randomness, chunk_size=chunk_size)


def vmap(fun: F,
         in_axes: int | None | Sequence[Any] = 0,
         out_axes: Any = 0,
         axis_name: AxisName | None = None,
         axis_size: int | None = None,
         spmd_axis_name: AxisName | tuple[AxisName, ...] | None = None,
         sum_match: bool = False
         ) -> F:
  """Vectorizing map. Creates a function which maps ``fun`` over argument axes.

  Args:
    fun: Function to be mapped over additional axes.
    in_axes: An integer, None, or sequence of values specifying which input
      array axes to map over.

      If each positional argument to ``fun`` is an array, then ``in_axes`` can
      be an integer, a None, or a tuple of integers and Nones with length equal
      to the number of positional arguments to ``fun``. An integer or ``None``
      indicates which array axis to map over for all arguments (with ``None``
      indicating not to map any axis), and a tuple indicates which axis to map
      for each corresponding positional argument. Axis integers must be in the
      range ``[-ndim, ndim)`` for each array, where ``ndim`` is the number of
      dimensions (axes) of the corresponding input array.

      If the positional arguments to ``fun`` are container (pytree) types, ``in_axes``
      must be a sequence with length equal to the number of positional arguments to
      ``fun``, and for each argument the corresponding element of ``in_axes`` can
      be a container with a matching pytree structure specifying the mapping of its
      container elements. In other words, ``in_axes`` must be a container tree prefix
      of the positional argument tuple passed to ``fun``. See this link for more detail:
      https://docs.jax.dev/en/latest/pytrees.html#applying-optional-parameters-to-pytrees

      Either ``axis_size`` must be provided explicitly, or at least one
      positional argument must have ``in_axes`` not None. The sizes of the
      mapped input axes for all mapped positional arguments must all be equal.

      Arguments passed as keywords are always mapped over their leading axis
      (i.e. axis index 0).

      See below for examples.

    out_axes: An integer, None, or (nested) standard Python container
      (tuple/list/dict) thereof indicating where the mapped axis should appear
      in the output. All outputs with a mapped axis must have a non-None
      ``out_axes`` specification. Axis integers must be in the range ``[-ndim,
      ndim)`` for each output array, where ``ndim`` is the number of dimensions
      (axes) of the array returned by the :func:`vmap`-ed function, which is one
      more than the number of dimensions (axes) of the corresponding array
      returned by ``fun``.
    axis_name: Optional, a hashable Python object used to identify the mapped
      axis so that parallel collectives can be applied.
    axis_size: Optional, an integer indicating the size of the axis to be
      mapped. If not provided, the mapped axis size is inferred from arguments.

  Returns:
    Batched/vectorized version of ``fun`` with arguments that correspond to
    those of ``fun``, but with extra array axes at positions indicated by
    ``in_axes``, and a return value that corresponds to that of ``fun``, but
    with extra array axes at positions indicated by ``out_axes``.

  For example, we can implement a matrix-matrix product using a vector dot
  product:

  >>> import jax.numpy as jnp
  >>>
  >>> vv = lambda x, y: jnp.vdot(x, y)  #  ([a], [a]) -> []
  >>> mv = vmap(vv, (0, None), 0)      #  ([b,a], [a]) -> [b]      (b is the mapped axis)
  >>> mm = vmap(mv, (None, 1), 1)      #  ([b,a], [a,c]) -> [b,c]  (c is the mapped axis)

  Here we use ``[a,b]`` to indicate an array with shape (a,b). Here are some
  variants:

  >>> mv1 = vmap(vv, (0, 0), 0)   #  ([b,a], [b,a]) -> [b]        (b is the mapped axis)
  >>> mv2 = vmap(vv, (0, 1), 0)   #  ([b,a], [a,b]) -> [b]        (b is the mapped axis)
  >>> mm2 = vmap(mv2, (1, 1), 0)  #  ([b,c,a], [a,c,b]) -> [c,b]  (c is the mapped axis)

  Here's an example of using container types in ``in_axes`` to specify which
  axes of the container elements to map over:

  >>> A, B, C, D = 2, 3, 4, 5
  >>> x = jnp.ones((A, B))
  >>> y = jnp.ones((B, C))
  >>> z = jnp.ones((C, D))
  >>> def foo(tree_arg):
  ...   x, (y, z) = tree_arg
  ...   return jnp.dot(x, jnp.dot(y, z))
  >>> tree = (x, (y, z))
  >>> print(foo(tree))
  [[12. 12. 12. 12. 12.]
   [12. 12. 12. 12. 12.]]
  >>> from jax import vmap
  >>> K = 6  # batch size
  >>> x = jnp.ones((K, A, B))  # batch axis in different locations
  >>> y = jnp.ones((B, K, C))
  >>> z = jnp.ones((C, D, K))
  >>> tree = (x, (y, z))
  >>> vfoo = vmap(foo, in_axes=((0, (1, 2)),))
  >>> print(vfoo(tree).shape)
  (6, 2, 5)

  Here's another example using container types in ``in_axes``, this time a
  dictionary, to specify the elements of the container to map over:

  >>> dct = {'a': 0., 'b': jnp.arange(5.)}
  >>> x = 1.
  >>> def foo(dct, x):
  ...  return dct['a'] + dct['b'] + x
  >>> out = vmap(foo, in_axes=({'a': None, 'b': 0}, None))(dct, x)
  >>> print(out)
  [1. 2. 3. 4. 5.]

  The results of a vectorized function can be mapped or unmapped. For example,
  the function below returns a pair with the first element mapped and the second
  unmapped. Only for unmapped results we can specify ``out_axes`` to be ``None``
  (to keep it unmapped).

  >>> print(vmap(lambda x, y: (x + y, y * 2.), in_axes=(0, None), out_axes=(0, None))(jnp.arange(2.), 4.))
  (Array([4., 5.], dtype=float32), 8.0)

  If the ``out_axes`` is specified for an unmapped result, the result is
  broadcast across the mapped axis:

  >>> print(vmap(lambda x, y: (x + y, y * 2.), in_axes=(0, None), out_axes=0)(jnp.arange(2.), 4.))
  (Array([4., 5.], dtype=float32), Array([8., 8.], dtype=float32, weak_type=True))

  If the ``out_axes`` is specified for a mapped result, the result is transposed
  accordingly.

  Finally, here's an example using ``axis_name`` together with collectives:

  >>> xs = jnp.arange(3. * 4.).reshape(3, 4)
  >>> print(vmap(lambda x: lax.psum(x, 'i'), axis_name='i')(xs))
  [[12. 15. 18. 21.]
   [12. 15. 18. 21.]
   [12. 15. 18. 21.]]

  See the :py:func:`jax.pmap` docstring for more examples involving collectives.
  """
  check_callable(fun)
  docstr = ("Vectorized version of {fun}. Takes similar arguments as {fun} "
            "but with additional array axes over which {fun} is mapped.")
  if fun.__doc__:
    docstr += "\n\nOriginal documentation:\n\n"
    docstr += fun.__doc__

  axis_name = core.no_axis_name if axis_name is None else axis_name
  if spmd_axis_name is not None and not isinstance(spmd_axis_name, tuple):
    spmd_axis_name = (spmd_axis_name,)

  if isinstance(in_axes, list):
    # To be a tree prefix of the positional args tuple, in_axes can never be a
    # list: if in_axes is not a leaf, it must be a tuple of trees. However,
    # in cases like these users expect tuples and lists to be treated
    # essentially interchangeably, so we canonicalize lists to tuples here
    # rather than raising an error. https://github.com/jax-ml/jax/issues/2367
    in_axes = tuple(in_axes)

  from jax._src import hijax  # pyrefly: ignore[missing-module-attribute]
  if not (in_axes is None or type(in_axes) in {int, tuple, *batching.spec_types}
          or isinstance(in_axes, hijax.MappingSpec)):
    raise TypeError("vmap in_axes must be an int, None, or a tuple of entries corresponding "
                    f"to the positional arguments passed to the function, but got {in_axes}.")
  if not all(type(l) in {int, *batching.spec_types} or isinstance(l, hijax.MappingSpec)
             for l in tree_leaves(in_axes)):
    raise TypeError("vmap in_axes must be an int, None, or (nested) container "
                    f"with those types as leaves, but got {in_axes}.")
  if not all(type(l) in {int, *batching.spec_types} or isinstance(l, hijax.MappingSpec)
             for l in tree_leaves(out_axes)):
    raise TypeError("vmap out_axes must be an int, None, or (nested) container "
                    f"with those types as leaves, but got {out_axes}.")

  @wraps(fun, docstr=docstr)
  @api_boundary
  def vmap_f(*args, **kwargs):
    nonlocal spmd_axis_name
    if isinstance(in_axes, tuple) and len(in_axes) != len(args):
      raise ValueError("vmap in_axes must be an int, None, or a tuple of entries corresponding "
                       "to the positional arguments passed to the function, "
                       f"but got {len(in_axes)=}, {len(args)=}")

    args_flat, in_tree  = tree_flatten((args, kwargs), is_leaf=batching.is_vmappable)
    dbg = debug_info("vmap", fun, args, kwargs)
    api_util.check_no_transformed_refs_args(lambda: dbg, args_flat)
    f = lu.wrap_init(fun, debug_info=dbg)
    flat_fun, out_tree = batching.flatten_fun_for_vmap(f, in_tree)
    in_axes_flat = flatten_axes("vmap in_axes", in_tree, (in_axes, 0), kws=True)

    if config.mutable_array_checks.value:
      avals = [None if d is None or batching.is_vmappable(x) else core.typeof(x)
               for x, d in zip(args_flat, in_axes_flat)]
      api_util.check_no_aliased_ref_args(lambda: dbg, avals, args_flat)

    axis_size_ = _mapped_axis_size(
        fun, in_tree, args_flat, in_axes_flat, "vmap", axis_size=axis_size)
    explicit_mesh_axis = _mapped_axis_spec(args_flat, in_axes_flat)
    _check_ema_unmapped_args(explicit_mesh_axis, args_flat, in_axes_flat)
    if spmd_axis_name is not None and explicit_mesh_axis is not None:
      if config.remove_size_one_mesh_axis_from_type.value:
        mesh = get_abstract_mesh()
        spmd_axis_name = tuple(i for i in spmd_axis_name if mesh.shape[i] != 1)
      if spmd_axis_name == explicit_mesh_axis:
        spmd_axis_name = None
      else:
        raise ValueError(
            "Only one of spmd_axis_name or arrays sharded on `Explicit` mesh"
            f" axis type is allowed. Got {spmd_axis_name=} and"
            f" arrays sharded on {explicit_mesh_axis=}")
      assert spmd_axis_name is None
    try:
      axis_data = batching.AxisData(axis_name, axis_size_, spmd_axis_name,
                                    explicit_mesh_axis)
      out_flat, inferred_out_axes = batching.batch(
          flat_fun, axis_data, in_axes_flat,
          lambda: flatten_axes("vmap out_axes", out_tree(), out_axes),
          sum_match=sum_match
      ).call_wrapped(*args_flat)
    except batching.SpecMatchError as e:
      out_axes_flat = flatten_axes("vmap out_axes", out_tree(), out_axes)
      out_axes_full = tree_unflatten(out_tree(), out_axes_flat)
      pairs, _ = tree_flatten_with_path(out_axes_full, is_leaf=lambda x: x is None)

      path, _ = pairs[e.leaf_idx]
      raise ValueError(f'at vmap out_axes{keystr(path)}, got axis spec {e.dst} '
                       f'but output was batched on axis {e.src}') from None
    if any(d is batching.infer for d in tree_leaves(out_axes)):
      return (tree_unflatten(out_tree(), out_flat),
              tree_unflatten(out_tree(), inferred_out_axes))
    else:
      return tree_unflatten(out_tree(), out_flat)

  return cast(F, vmap_f)


def vmap(
  fn: Callable[..., Any],
  variable_axes: Mapping[CollectionFilter, InOutAxis],
  split_rngs: Mapping[PRNGSequenceFilter, bool],
  in_axes=0,
  out_axes=0,
  axis_size: int | None = None,
  axis_name: str | None = None,
  spmd_axis_name: str | None = None,
  metadata_params: dict[Any, Any] = {},
) -> Callable[..., Any]:
  """A lifted version of ``jax.vmap``.

  See ``jax.vmap`` for the unlifted batch transform in Jax.

  ``vmap`` can be used to add a batch axis to a scope function.
  For example we could create a version of ``dense`` with
  a batch axis that does not share parameters::

    batch_dense = lift.vmap(
        nn.dense,
        in_axes=(0, None),
        variable_axes={'params': 0},
        split_rngs={'params': True})

  By using ``variable_axes={'params': 0}``, we indicate that the
  parameters themselves are mapped over and therefore not shared along
  the mapped axis. Consequently, we also split the 'params' RNG,
  otherwise the parameters would be initialized identically along
  the mapped axis.

  Similarly, ``vmap`` could be use to add a batch axis with parameter
  sharing::

    batch_foo = lift.vmap(
        foo,
        in_axes=0, out_axes=0,
        variable_axes={'params': None},
        split_rngs={'params': False})

  Here we use ``variable_axes={'params': None}`` to indicate the parameter
  variables are shared along the mapped axis. Consequently, the 'params'
  RNG must also be shared.

  Args:
    fn: the function to be transformed.
    variable_axes: the variable collections that are lifted into the batching
      transformation. Use `None` to indicate a broadcasted collection or an
      integer to map over an axis.
    split_rngs: Split PRNG sequences will be different for each index of the
      batch dimension. Unsplit PRNGs will be broadcasted.
    in_axes: Specifies the mapping of the input arguments (see `jax.vmap).
    out_axes: Specifies the mapping of the return value (see `jax.vmap).
    axis_size: Specifies the size of the batch axis. This only needs to be
      specified if it cannot be derived from the input arguments.
    axis_name: Specifies a name for the batch axis. Can be used together with
      parallel reduction primitives (e.g. `jax.lax.pmean`, `jax.lax.ppermute`,
      etc.). Note, this is only used for pmap and shmap. For SPMD jit, you do
      not need to manually synchronize. Just make sure that the axes are
      correctly annotated and XLA:SPMD will insert the necessary collectives.
    spmd_axis_name: Axis name added to any pjit sharding constraints appearing
      in `fn`. See also
      https://github.com/google/flax/blob/main/flax/linen/partitioning.py.
    metadata_params: arguments dict passed to AxisMetadata instances in the
      variable tree.

  Returns:
    A vectorized version of the input scope function.
  """
  variable_in_axes, variable_out_axes = _split_in_out_axes(variable_axes)
  variable_in_groups, variable_in_axes = _unzip2(variable_in_axes.items())
  variable_out_groups, variable_out_axes = _unzip2(variable_out_axes.items())
  rng_groups, rng_splits = _unzip2(split_rngs.items())
  rng_axes = tuple(0 if rng_split else None for rng_split in rng_splits)

  def inner(scope_fn, repack_fn, variable_groups, rng_groups, *args):
    # optional user-defined variable transform on the way in
    new_variable_groups = []
    for var_group, axis in zip(variable_groups, variable_in_axes):
      if axis is not None:
        new_variable_groups.append(
            meta.remove_axis(var_group, axis, metadata_params)
        )
      else:
        new_variable_groups.append(var_group)
    variable_groups = tuple(new_variable_groups)

    # split rngs
    def find_axis_size(axis, x):
      if axis is not None:
        leaves = jax.tree_util.tree_leaves(x)
        if leaves:
          return leaves[0].shape[axis]
      return ()

    axis_sizes = jax.tree_util.tree_map(
        find_axis_size, (variable_in_axes, in_axes), (variable_groups, args),
        is_leaf=lambda x: x is None
    )
    axis_sizes = set(jax.tree_util.tree_leaves(axis_sizes))
    if axis_size is None and len(axis_sizes) == 1:
      (d_axis_size,) = axis_sizes
    elif len(axis_sizes) > 1:
      raise ValueError(f'Inconsistent batch axis sizes: {axis_sizes}')
    elif axis_size is None:
      raise ValueError('axis_size should be specified manually.')
    else:
      d_axis_size = axis_size

    def split_fn(rng):
      # random.clone is only available on Jax versions 0.4.26 or newer. See:
      # https://jax.readthedocs.io/en/latest/jax.experimental.key_reuse.htmls
      if hasattr(random, 'clone'):
        rng = random.clone(rng)
      rngs = random.split(rng, d_axis_size)
      if spmd_axis_name is not None:
        args_flat, _ = jax.tree.flatten(args)
        axes_flat = _broadcast_prefix_tree(in_axes, args)
        any_vmapped_axis_sharded = any(
            jax.typeof(x).sharding.spec[i] == spmd_axis_name
            for x, i in zip(args_flat, axes_flat)
            if i is not None
        )
        if any_vmapped_axis_sharded:
          rngs = jax.sharding.reshard(rngs, jax.P(spmd_axis_name))
      return rngs

    rng_groups = tuple(
        tree_map_rngs(split_fn, rng_group) if split else rng_group
        for rng_group, split in zip(rng_groups, rng_splits)
    )

    @functools.partial(
        jax.vmap,
        in_axes=(variable_in_axes, rng_axes, in_axes),
        out_axes=(out_axes, variable_out_axes),
        axis_name=axis_name,
        axis_size=axis_size,
        spmd_axis_name=spmd_axis_name,
    )
    @functools.wraps(fn)
    def mapped(variable_groups, rng_groups, args):
      scope = scope_fn(variable_groups, rng_groups)
      y = fn(scope, *args)
      return y, repack_fn(scope)

    # optional user-defined variable transform on the way out
    y, vars_out = mapped(variable_groups, rng_groups, args)
    new_vars_out = []
    for var_group, axis in zip(vars_out, variable_out_axes):
      if axis is not None:
        new_vars_out.append(meta.add_axis(var_group, axis, metadata_params))
      else:
        new_vars_out.append(var_group)
    vars_out = tuple(new_vars_out)
    return y, vars_out

  return pack(
    inner, variable_in_groups, variable_out_groups, rng_groups, name='vmap'
  )


def vmap(
  target: Target,
  variable_axes: Mapping[CollectionFilter, InOutAxis] = FrozenDict(),
  split_rngs: Mapping[PRNGSequenceFilter, bool] = FrozenDict(),
  in_axes=0,
  out_axes=0,
  axis_size: int | None = None,
  axis_name: str | None = None,
  spmd_axis_name: str | None = None,
  metadata_params: Mapping[Any, Any] = {},
  methods=None,
) -> Target:
  """A lifted version of ``jax.vmap``.

  See ``jax.vmap`` for the unlifted batch transform in Jax.

  ``vmap`` can be used to add a batch axis to a ``Module``.
  For example we could create a version of ``Dense`` with
  a batch axis that does not share parameters::

    >>> import flax.linen as nn
    >>> BatchDense = nn.vmap(
    ...     nn.Dense,
    ...     in_axes=0, out_axes=0,
    ...     variable_axes={'params': 0},
    ...     split_rngs={'params': True})

  By using ``variable_axes={'params': 0}``, we indicate that the
  parameters themselves are mapped over and therefore not shared along
  the mapped axis. Consequently, we also split the 'params' RNG,
  otherwise the parameters would be initialized identically along
  the mapped axis.

  Similarly, ``vmap`` could be used to add a batch axis with parameter
  sharing::

    >>> import flax.linen as nn
    >>> BatchDense = nn.vmap(
    ...     nn.Dense,
    ...     in_axes=0, out_axes=0,
    ...     variable_axes={'params': None},
    ...     split_rngs={'params': False})

  Here we use ``variable_axes={'params': None}`` to indicate the parameter
  variables are shared along the mapped axis. Consequently, the 'params'
  RNG must also be shared.

  Args:
    target: a ``Module`` or a function taking a ``Module`` as its first
      argument.
    variable_axes: the variable collections that are lifted into the batching
      transformation. Use ``None`` to indicate a broadcasted collection or an
      integer to map over an axis. For example, passing in
      ``variable_axes={'params': None}`` will indicate that the
      parameter variables should be shared along the mapped axis.
    split_rngs: Split PRNG sequences will be different for each index of the
      batch dimension. Unsplit PRNGs will be broadcasted.
    in_axes: Specifies the mapping of the input arguments (see ``jax.vmap``).
    out_axes: Specifies the mapping of the return value (see ``jax.vmap``).
    axis_size: Specifies the size of the batch axis. This only needs to be
      specified if it cannot be derived from the input arguments.
    axis_name: Specifies a name for the batch axis. Can be used together with
      parallel reduction primitives (e.g. ``jax.lax.pmean``, ``jax.lax.ppermute``,
      etc.). Note, this is only used for pmap and shard map. For SPMD jit, you
      do not need to manually synchronize. Just make sure that the axes are
      correctly annotated and XLA:SPMD will insert the necessary collectives.
    methods: If ``target`` is a ``Module``, the methods of ``Module`` to vmap over.
    spmd_axis_name: Axis name added to any pjit sharding constraints appearing
      in ``fn``. See also
      https://github.com/google/flax/blob/main/flax/linen/partitioning.py.
    metadata_params: arguments dict passed to AxisMetadata instances in the
      variable tree.

  Returns:
    A batched/vectorized version of ``target``, with the same arguments but with
    extra axes at positions indicated by ``in_axes``, and the same return value,
    but with extra axes at positions indicated by ``out_axes``.
  """
  return lift_transform(
    lift.vmap,
    target,
    variable_axes,
    split_rngs,
    methods=methods,
    in_axes=in_axes,
    out_axes=out_axes,
    axis_size=axis_size,
    axis_name=axis_name,
    metadata_params=metadata_params,
    spmd_axis_name=spmd_axis_name,
  )


def vmap(
    *,
    in_axes: int | None | tp.Sequence[tp.Any] = 0,
    out_axes: tp.Any = 0,
    axis_name: AxisName | None = None,
    axis_size: int | None = None,
    spmd_axis_name: AxisName | tuple[AxisName, ...] | None = None,
    # nnx specific
    transform_metadata: tp.Mapping[str, tp.Any] = FrozenDict({}),
    graph: bool | None = None,
    graph_updates: bool | None = None,
) -> tp.Callable[[F], F]:
  ...


def vmap(
    f: F,
    *,
    in_axes: int | None | tp.Sequence[tp.Any] = 0,
    out_axes: tp.Any = 0,
    axis_name: AxisName | None = None,
    axis_size: int | None = None,
    spmd_axis_name: AxisName | tuple[AxisName, ...] | None = None,
    # nnx specific
    transform_metadata: tp.Mapping[str, tp.Any] = FrozenDict({}),
    graph: bool | None = None,
    graph_updates: bool | None = None,
) -> F:
  ...


def vmap(
  f: F | type[Missing] = Missing,
  *,
  in_axes: int | None | tp.Sequence[tp.Any] = 0,
  out_axes: tp.Any = 0,
  axis_name: AxisName | None = None,
  axis_size: int | None = None,
  spmd_axis_name: AxisName | tuple[AxisName, ...] | None = None,
  # nnx specific
  transform_metadata: tp.Mapping[str, tp.Any] = FrozenDict({}),
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> F | tp.Callable[[F], F]:
  """Reference-aware version of `jax.vmap <https://jax.readthedocs.io/en/latest/_autosummary/jax.vmap.html>`__.

  Args:
    f: Function to be mapped over additional axes.
    in_axes: An integer, None, or sequence of values specifying which input
      array axes to map over (see `jax.vmap
      <https://jax.readthedocs.io/en/latest/_autosummary/jax.vmap.html>`__). In
      addition to integers and None, :class:`StateAxes`  can be used to control
      how graph nodes like Modules are vectorized by specifying the axes to be
      applied to substates of the graph node given a `Filter
      <https://flax.readthedocs.io/en/latest/guides/filters_guide.html>`__.
    out_axes: An integer, None, or pytree indicating where the mapped axis
      should appear in the output (see `jax.vmap
      <https://jax.readthedocs.io/en/latest/_autosummary/jax.vmap.html>`__).
    axis_name: Optional, a hashable Python object used to identify the mapped
      axis so that parallel collectives can be applied.
    axis_size: Optional, an integer indicating the size of the axis to be
      mapped. If not provided, the mapped axis size is inferred from arguments.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references and reference semantics.
      If ``False``, uses tree-mode which treats Modules as regular JAX
      pytrees, avoiding the overhead of the graph protocol. Tree-mode does
      not support ``StateAxes`` or shared ``Variable`` references.
    graph_updates: If ``True``, propagates updates on graph structure
      that happen inside the transform to the input graphs, has no
      effect when ``graph=False``. When ``False``, using ``StateAxes``
      is not supported.

  Returns:
    Batched/vectorized version of ``f`` with arguments that correspond to
    those of ``f``, but with extra array axes at positions indicated by
    ``in_axes``, and a return value that corresponds to that of ``f``, but
    with extra array axes at positions indicated by ``out_axes``.

  Example::

    >>> from flax import nnx
    >>> from jax import random, numpy as jnp
    ...
    >>> model = nnx.Linear(2, 3, rngs=nnx.Rngs(0))
    >>> x = jnp.ones((5, 2))
    ...
    >>> @nnx.vmap(in_axes=(None, 0), out_axes=0)
    ... def forward(model, x):
    ...   return model(x)
    ...
    >>> y = forward(model, x)
    >>> y.shape
    (5, 3)

  >>> class LinearEnsemble(nnx.Module):
  ...   def __init__(self, num, rngs):
  ...     self.w = nnx.Param(jax.random.uniform(rngs(), (num, 2, 3)))
  ...
  >>> model = LinearEnsemble(5, rngs=nnx.Rngs(0))
  >>> x = jnp.ones((2,))
  ...
  >>> @nnx.vmap(in_axes=(0, None), out_axes=0)
  ... def forward(model, x):
  ...   return x @ model.w
  ...
  >>> y = forward(model, x)
  >>> y.shape
  (5, 3)

  To control control how graph node substates are vectorized, ``StateAxes``
  can be passed to ``in_axes`` and ``out_axes`` specifying the axes to be
  applied to each substate given a filter. The following example shows how to
  share the parameters between the ensemble members which keeping different
  batch statistics and dropout random state::

    >>> class Foo(nnx.Module):
    ...   def __init__(self):
    ...     self.a = nnx.Param(jnp.arange(4))
    ...     self.b = nnx.BatchStat(jnp.arange(4))
    ...
    >>> state_axes = nnx.StateAxes({nnx.Param: 0, nnx.BatchStat: None})
    >>> @nnx.vmap(in_axes=(state_axes,), out_axes=0)
    ... def mul(foo):
    ...   return foo.a * foo.b
    ...
    >>> foo = Foo()
    >>> y = mul(foo)
    >>> y
    Array([[0, 0, 0, 0],
           [0, 1, 2, 3],
           [0, 2, 4, 6],
           [0, 3, 6, 9]], dtype=int32)
  """
  if graph is None:
    graph = graphlib.set_graph_mode.current_value()
  if graph_updates is None:
    graph_updates = graphlib.set_graph_updates.current_value()
  if f is Missing:
    return functools.partial(
        vmap,
        in_axes=in_axes,
        out_axes=out_axes,
        axis_name=axis_name,
        axis_size=axis_size,
        spmd_axis_name=spmd_axis_name,
        transform_metadata=transform_metadata,
        graph=graph,
        graph_updates=graph_updates,
    )  # type: ignore[return-value]

  f_unbound, _, was_bound = _resolve_bound_callable(f)
  if was_bound:
    _raise_bound_method_error('vmap')

  extract.check_prefix(in_axes, 'in_axes', 'vmap', graph, graph_updates)
  extract.check_prefix(out_axes, 'out_axes', 'vmap', graph, graph_updates)

  if not (graph and graph_updates):

    vmapped_fn = jax.vmap(
      SimpleVmapFn(f_unbound, graph=graph, out_axes=out_axes),
      in_axes=in_axes,
      out_axes=(out_axes, (in_axes, 0)),
      axis_name=axis_name,
      axis_size=axis_size,
      spmd_axis_name=spmd_axis_name,
    )

    @functools.wraps(f_unbound)
    def simple_vmap_wrapper(*args, **kwargs):
      if graph:
        args, kwargs = extract.to_tree2(
            (args, kwargs),
            prefix=(in_axes, None)
            if in_axes is not None
            else None,
            check_aliasing=in_axes is not None,
        )
      extract.check_no_aliases('vmap', args=args, kwargs=kwargs)
      out, updates = vmapped_fn(*args, **kwargs)
      extract.apply_variable_updates((args, kwargs), updates)
      if graph:
        out = extract.from_tree2(out)
      return out

    return simple_vmap_wrapper  # type: ignore[return-value]


  jax_in_axes = jax.tree.map(
    lambda x: extract.NodeStates.from_prefixes(x.axes, metadata=x)
    if isinstance(x, StateAxes)
    else x,
    in_axes,
  )
  jax_out_axes = jax.tree.map(
    lambda x: extract.NodeStates.from_prefixes(x.axes, metadata=x)
    if isinstance(x, StateAxes)
    else x,
    out_axes,
  )
  vmapped_fn = jax.vmap(  # type: ignore[assignment]
      VmapFn(f_unbound, transform_metadata, in_axes, out_axes),
      in_axes=jax_in_axes,
      out_axes=(jax_in_axes, jax_out_axes),
      axis_name=axis_name,
      axis_size=axis_size,
      spmd_axis_name=spmd_axis_name,
  )

  @functools.wraps(f)
  @graphlib.update_context('vmap')
  def vmap_wrapper(*args, **kwargs):
    args = resolve_kwargs(f, args, kwargs)
    pure_args = extract.to_tree(
        args, prefix=in_axes, split_fn=_vmap_split_fn, ctxtag='vmap'
    )
    pure_args_out, pure_out = vmapped_fn(*pure_args)
    _args_out, out = extract.from_tree(
      (pure_args_out, pure_out), ctxtag='vmap', is_inner=False
    )
    return out

  return vmap_wrapper  # type: ignore

