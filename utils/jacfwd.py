
def jacfwd(
    func: Callable[..., Any],
    argnums: argnums_t = 0,
    has_aux: bool = False,
    *,
    randomness: str = "error",
) -> Callable[..., Any]:
    warn_deprecated("jacfwd")
    return _impl.jacfwd(func, argnums, has_aux, randomness=randomness)


def jacfwd(
    func: Callable[..., Any],
    argnums: argnums_t = 0,
    has_aux: bool = False,
    *,
    randomness: str = "error",
) -> Callable[..., Any]:
    """
    Computes the Jacobian of ``func`` with respect to the arg(s) at index
    ``argnum`` using forward-mode autodiff

    Args:
        func (function): A Python function that takes one or more arguments,
            one of which must be a Tensor, and returns one or more Tensors
        argnums (int or tuple[int, ...]): Optional, integer or tuple of integers,
            saying which arguments to get the Jacobian with respect to.
            Default: 0.
        has_aux (bool): Flag indicating that ``func`` returns a
            ``(output, aux)`` tuple where the first element is the output of
            the function to be differentiated and the second element is
            auxiliary objects that will not be differentiated.
            Default: False.
        randomness(str): Flag indicating what type of randomness to use.
            See :func:`vmap` for more detail. Allowed: "different", "same", "error".
            Default: "error"

    Returns:
        Returns a function that takes in the same inputs as ``func`` and
        returns the Jacobian of ``func`` with respect to the arg(s) at
        ``argnums``. If ``has_aux is True``, then the returned function
        instead returns a ``(jacobian, aux)`` tuple where ``jacobian``
        is the Jacobian and ``aux`` is auxiliary objects returned by ``func``.

    .. note::
        You may see this API error out with "forward-mode AD not implemented
        for operator X". If so, please file a bug report and we will prioritize it.
        An alternative is to use :func:`jacrev`, which has better operator coverage.

    A basic usage with a pointwise, unary operation will give a diagonal array
    as the Jacobian

        >>> from torch.func import jacfwd
        >>> x = torch.randn(5)
        >>> jacobian = jacfwd(torch.sin)(x)
        >>> expected = torch.diag(torch.cos(x))
        >>> assert torch.allclose(jacobian, expected)

    :func:`jacfwd` can be composed with vmap to produce batched
    Jacobians:

        >>> from torch.func import jacfwd, vmap
        >>> x = torch.randn(64, 5)
        >>> jacobian = vmap(jacfwd(torch.sin))(x)
        >>> assert jacobian.shape == (64, 5, 5)

    If you would like to compute the output of the function as well as the
    jacobian of the function, use the ``has_aux`` flag to return the output
    as an auxiliary object:

        >>> from torch.func import jacfwd
        >>> x = torch.randn(5)
        >>>
        >>> def f(x):
        >>>   return x.sin()
        >>>
        >>> def g(x):
        >>>   result = f(x)
        >>>   return result, result
        >>>
        >>> jacobian_f, f_x = jacfwd(g, has_aux=True)(x)
        >>> assert torch.allclose(f_x, f(x))

    Additionally, :func:`jacrev` can be composed with itself or :func:`jacrev`
    to produce Hessians

        >>> from torch.func import jacfwd, jacrev
        >>> def f(x):
        >>>   return x.sin().sum()
        >>>
        >>> x = torch.randn(5)
        >>> hessian = jacfwd(jacrev(f))(x)
        >>> assert torch.allclose(hessian, torch.diag(-x.sin()))

    By default, :func:`jacfwd` computes the Jacobian with respect to the first
    input. However, it can compute the Jacboian with respect to a different
    argument by using ``argnums``:

        >>> from torch.func import jacfwd
        >>> def f(x, y):
        >>>   return x + y ** 2
        >>>
        >>> x, y = torch.randn(5), torch.randn(5)
        >>> jacobian = jacfwd(f, argnums=1)(x, y)
        >>> expected = torch.diag(2 * y)
        >>> assert torch.allclose(jacobian, expected)

    Additionally, passing a tuple to ``argnums`` will compute the Jacobian
    with respect to multiple arguments

        >>> from torch.func import jacfwd
        >>> def f(x, y):
        >>>   return x + y ** 2
        >>>
        >>> x, y = torch.randn(5), torch.randn(5)
        >>> jacobian = jacfwd(f, argnums=(0, 1))(x, y)
        >>> expectedX = torch.diag(torch.ones_like(x))
        >>> expectedY = torch.diag(2 * y)
        >>> assert torch.allclose(jacobian[0], expectedX)
        >>> assert torch.allclose(jacobian[1], expectedY)

    """

    @wraps(func)
    def wrapper_fn(*args: Any) -> Any:
        error_if_complex("jacfwd", args, is_input=True)
        primals = args if argnums is None else _slice_argnums(args, argnums)
        flat_primals, primals_spec = tree_flatten(primals)
        flat_primals_numels = tuple(p.numel() for p in flat_primals)
        flat_basis = _construct_standard_basis_for(flat_primals, flat_primals_numels)
        if flat_basis is None:
            raise AssertionError("flat_basis must not be None")
        basis = tree_unflatten(flat_basis, primals_spec)

        def push_jvp(basis: Any) -> Any:
            output = _jvp_with_argnums(
                func, args, basis, argnums=argnums, has_aux=has_aux
            )
            # output[0] is the output of `func(*args)`
            error_if_complex("jacfwd", output[0], is_input=False)
            if has_aux:
                _, jvp_out, aux = output  # pyrefly: ignore[bad-unpacking]
                return jvp_out, aux
            _, jvp_out = output  # pyrefly: ignore[bad-unpacking]
            return jvp_out

        results = vmap(push_jvp, randomness=randomness)(basis)
        aux: Any = None
        if has_aux:
            results, aux = results
            # aux is in the standard basis format, e.g. NxN matrix
            # We need to fetch the first element as original `func` output
            flat_aux, aux_spec = tree_flatten(aux)
            flat_aux = [value[0] for value in flat_aux]
            aux = tree_unflatten(flat_aux, aux_spec)

        jac_outs, spec = tree_flatten(results)
        # Most probably below output check can never raise an error
        # as jvp should test the output before
        # assert_non_empty_output(jac_outs, 'jacfwd(f, ...)(*args)')

        jac_outs_ins = tuple(
            tuple(
                safe_unflatten(jac_out_in, -1, primal.shape)
                for primal, jac_out_in in zip(
                    flat_primals,
                    jac_out.movedim(0, -1).split(flat_primals_numels, dim=-1),
                )
            )
            for jac_out in jac_outs
        )
        jac_outs_ins = tuple(
            tree_unflatten(jac_ins, primals_spec) for jac_ins in jac_outs_ins
        )

        if isinstance(argnums, int):
            jac_outs_ins = tuple(jac_ins[0] for jac_ins in jac_outs_ins)
        if has_aux:
            return tree_unflatten(jac_outs_ins, spec), aux  # type: ignore[possibly-unbound]
        return tree_unflatten(jac_outs_ins, spec)

    return wrapper_fn


def jacfwd(fun: Callable, argnums: int | Sequence[int] = 0,
           has_aux: bool = False, holomorphic: bool = False) -> Callable:
  """Jacobian of ``fun`` evaluated column-by-column using forward-mode AD.

  Args:
    fun: Function whose Jacobian is to be computed.
    argnums: Optional, integer or sequence of integers. Specifies which
      positional argument(s) to differentiate with respect to (default ``0``).
    has_aux: Optional, bool. Indicates whether ``fun`` returns a pair where the
      first element is considered the output of the mathematical function to be
      differentiated and the second element is auxiliary data. Default False.
    holomorphic: Optional, bool. Indicates whether ``fun`` is promised to be
      holomorphic. Default False.

  Returns:
    A function with the same arguments as ``fun``, that evaluates the Jacobian of
    ``fun`` using forward-mode automatic differentiation. If ``has_aux`` is True
    then a pair of (jacobian, auxiliary_data) is returned.

  >>> import jax
  >>> import jax.numpy as jnp
  >>>
  >>> def f(x):
  ...   return jnp.asarray(
  ...     [x[0], 5*x[2], 4*x[1]**2 - 2*x[2], x[2] * jnp.sin(x[0])])
  ...
  >>> print(jax.jacfwd(f)(jnp.array([1., 2., 3.])))
  [[ 1.       0.       0.     ]
   [ 0.       0.       5.     ]
   [ 0.      16.      -2.     ]
   [ 1.6209   0.       0.84147]]
  """
  check_callable(fun)
  argnums = _ensure_index(argnums)

  docstr = ("Jacobian of {fun} with respect to positional argument(s) "
            "{argnums}. Takes the same arguments as {fun} but returns the "
            "jacobian of the output with respect to the arguments at "
            "positions {argnums}.")

  @wraps(fun, docstr=docstr, argnums=argnums)
  def jacfun(*args, **kwargs):
    f_partial, dyn_args = argnums_partial2(fun, argnums, args, kwargs)
    tree_map(partial(_check_input_dtype_jacfwd, holomorphic), dyn_args)
    pushfwd: Callable = partial(_jvp, f_partial, dyn_args, has_aux=has_aux)
    if has_aux:
      y, jac, aux = vmap(pushfwd, out_axes=(None, -1, None))(_std_basis(dyn_args))
    else:
      y, jac = vmap(pushfwd, out_axes=(None, -1))(_std_basis(dyn_args))
      aux = None
    tree_map(partial(_check_output_dtype_jacfwd, holomorphic), y)
    example_args = dyn_args[0] if isinstance(argnums, int) else dyn_args
    jac_tree = tree_map(partial(_jacfwd_unravel, example_args), y, jac)
    if not has_aux:
      return jac_tree
    else:
      return jac_tree, aux

  return jacfun


def jacfwd(fun: Callable, argnums: int | Sequence[int] = 0,
           has_aux: bool = False, **kwargs) -> Callable:
  """Sparse-aware version of :func:`jax.jacfwd`

  Arguments and return values are the same as :func:`jax.jacfwd`, but when taking
  the gradient with respect to a :class:`jax.experimental.sparse` array, the
  gradient is computed in the subspace defined by the array's sparsity pattern.
  Currently this is only implemented for dense outputs.
  """
  raw_jacfwd_fun = jax.jacfwd(fun, argnums=argnums, **kwargs)
  argnums = core.concrete_or_error(_ensure_index, argnums)

  @wraps(fun, docstr=raw_jacfwd_fun.__doc__, argnums=argnums)
  @api_boundary
  def jacfwd_fun(*args, **kwargs):
    fun_flat, argnums_flat, args_flat, postprocess_gradients = flatten_fun_for_sparse_ad(fun, argnums, args)
    out = jax.jacfwd(fun_flat, argnums=argnums_flat, has_aux=has_aux, **kwargs)(*args_flat)
    if has_aux:
      return postprocess_gradients(out[0]), out[1]
    return postprocess_gradients(out)
  return jacfwd_fun

