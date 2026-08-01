
def value_and_grad(fun: Callable, argnums: int | Sequence[int] = 0,
                   has_aux: bool = False, holomorphic: bool = False,
                   allow_int: bool = False, reduce_axes: Sequence[AxisName] = ()
  ) -> Callable[..., tuple[Any, Any]]:
  """Create a function that evaluates both ``fun`` and the gradient of ``fun``.

  Args:
    fun: Function to be differentiated. Its arguments at positions specified by
      ``argnums`` should be arrays, scalars, or standard Python containers. It
      should return a scalar (which includes arrays with shape ``()`` but not
      arrays with shape ``(1,)`` etc.)
    argnums: Optional, integer or sequence of integers. Specifies which
      positional argument(s) to differentiate with respect to (default 0).
    has_aux: Optional, bool. Indicates whether ``fun`` returns a pair where the
      first element is considered the output of the mathematical function to be
      differentiated and the second element is auxiliary data. Default False.
    holomorphic: Optional, bool. Indicates whether ``fun`` is promised to be
      holomorphic. If True, inputs and outputs must be complex. Default False.
    allow_int: Optional, bool. Whether to allow differentiating with
      respect to integer valued inputs. The gradient of an integer input will
      have a trivial vector-space dtype (float0). Default False.

  Returns:
    A function with the same arguments as ``fun`` that evaluates both ``fun``
    and the gradient of ``fun`` and returns them as a pair (a two-element
    tuple). If ``argnums`` is an integer then the gradient has the same shape
    and type as the positional argument indicated by that integer. If argnums is
    a sequence of integers, the gradient is a tuple of values with the same
    shapes and types as the corresponding arguments. If ``has_aux`` is True
    then a tuple of ((value, auxiliary_data), gradient) is returned.
  """
  from jax._src.lax import lax as lax_internal  # pyrefly: ignore[missing-import]

  if reduce_axes:
    raise NotImplementedError("reduce_axes argument to grad is deprecated")
  del reduce_axes

  docstr = ("Value and gradient of {fun} with respect to positional "
            "argument(s) {argnums}. Takes the same arguments as {fun} but "
            "returns a two-element tuple where the first element is the value "
            "of {fun} and the second element is the gradient, which has the "
            "same shape as the arguments at positions {argnums}.")

  check_callable(fun)
  argnums = core.concrete_or_error(_ensure_index, argnums)

  @wraps(fun, docstr=docstr, argnums=argnums)
  @api_boundary
  def value_and_grad_f(*args, **kwargs):
    max_argnum = argnums if isinstance(argnums, int) else max(argnums)
    if max_argnum >= len(args):
      raise TypeError(f"differentiating with respect to {argnums=} requires at least "
                      f"{max_argnum + 1} positional arguments to be passed by the caller, "
                      f"but got only {len(args)} positional arguments.")
    f_partial, dyn_args = argnums_partial2(fun, argnums, args, kwargs)
    for leaf in tree_leaves(dyn_args):
      _check_input_dtype_grad(holomorphic, allow_int, leaf)
    ans, vjp_py, *maybe_aux = vjp(f_partial, *dyn_args, has_aux=has_aux)
    _check_scalar(ans)
    tree_map(partial(_check_output_dtype_grad, holomorphic), ans)
    g = vjp_py(lax_internal._one_vjp(ans))
    g = g[0] if isinstance(argnums, int) else g
    ans_aux = (ans, *maybe_aux) if has_aux else ans
    return ans_aux, g

  return value_and_grad_f


def value_and_grad(fun: Callable, argnums: int | Sequence[int] = 0,
                   has_aux=False, **kwargs) -> Callable[..., tuple[Any, Any]]:
  """Sparse-aware version of :func:`jax.value_and_grad`

  Arguments and return values are the same as :func:`jax.value_and_grad`, but when
  taking the gradient with respect to a :class:`jax.experimental.sparse` array, the
  gradient is computed in the subspace defined by the array's sparsity pattern.

  Examples:

    >>> from jax.experimental import sparse
    >>> X = sparse.BCOO.fromdense(jnp.arange(6.))
    >>> y = jnp.ones(6)
    >>> sparse.value_and_grad(lambda X, y: X @ y)(X, y)
    (Array(15., dtype=float32), BCOO(float32[6], nse=5))
  """
  raw_value_and_grad_fun = jax.value_and_grad(fun, argnums=argnums, has_aux=has_aux, **kwargs)
  argnums = core.concrete_or_error(_ensure_index, argnums)

  @wraps(fun, docstr=raw_value_and_grad_fun.__doc__, argnums=argnums)
  @api_boundary
  def value_and_grad_fun(*args, **kwargs):
    fun_flat, argnums_flat, args_flat, postprocess_gradients = flatten_fun_for_sparse_ad(fun, argnums, args)
    val_out, grad_out = jax.value_and_grad(fun_flat, argnums=argnums_flat, has_aux=has_aux, **kwargs)(*args_flat)
    return val_out, postprocess_gradients(grad_out)
  return value_and_grad_fun


def value_and_grad(
  fn: Callable[..., Any],
  scope: Scope,
  *primals,
  has_aux: bool = False,
  reduce_axes=(),
  variables: CollectionFilter = True,
  rngs: PRNGSequenceFilter = True,
) -> tuple[Any, Callable[..., Any]] | tuple[Any, Callable[..., Any], Any]:
  """A limited lifted version of ``jax.value_and_grad``.

  See ``jax.value_and_grad`` for the unlifted reverse mode gradient.

  Note that for this convenience function, gradients are only calculated for
  the function inputs (all function inputs), and not with respect to any scope
  variables. The target function must return a scalar-valued output.

  Example::

    def learn_scale(scope, x, y):
      p = scope.param('scale', nn.initializers.zeros_init(), ())
      return p * x * y
    def f(scope, x, y):
      z, x_grad, y_grad = lift.value_and_grad(learn_scale, scope, x, y)
      return z, x_grad, y_grad

  Args:
    fn: Function to be differentiated. Its arguments should be arrays, scalars,
      or standard Python containers of arrays or scalars. It should return an
      array, scalar, or standard Python container of arrays or scalars. It will
      receive the scope and primals as arguments.
    scope: The scope of which the variables will be differentiated.
    *primals: A sequence of primal values at which the Jacobian of ``fn``
      should be evaluated. The length of ``primals`` should be equal to the
      number of positional parameters to ``fn``. Each primal value should be a
      tuple of arrays, scalar, or standard Python containers thereof.
    has_aux: Optional, bool. Indicates whether ``fn`` returns a pair where the
     first element is considered the output of the mathematical function to be
     differentiated and the second element is auxiliary data. Default ``False``.
    variables: other variables collections that are available inside `fn` but
      do not receive a cotangent.
    rngs: the prngs that are available inside `fn`.

  Returns:
    If ``has_aux`` is ``False``, returns a ``(primals_out, grads)`` pair, where
    ``primals_out`` is ``fn(*primals)``.
    If ``has_aux`` is ``True``, returns a
    ``(primals_out, aux, grads)`` tuple where ``aux`` is the auxiliary data
    returned by ``fn``.
  """
  if reduce_axes:
    raise NotImplementedError(
        'reduce_axes argument to value_and_grad is deprecated')
  del reduce_axes

  def inner(scope_fn, repack_fn, variable_groups, rng_groups, *args):
    @functools.wraps(fn)
    def wrapper(*args):
      scope = scope_fn(variable_groups, rng_groups)
      if has_aux:
        y, aux = fn(scope, *args)
      else:
        y = fn(scope, *args)
        aux = ()
      return y, (aux, repack_fn(scope))

    y, bwd, (aux, out_vars) = jax.vjp(
      wrapper,
      *args,
      has_aux=True,
    )

    inputs_grad = bwd(jax.numpy.ones_like(y))

    if has_aux:
      return (y, aux, inputs_grad), out_vars
    else:
      return (y, inputs_grad), out_vars

  return pack(
    inner,
    (variables,),
    (variables,),
    (rngs,),
    name='value_and_grad',
    enable_kwargs=False,
  )(scope, *primals)


def value_and_grad(
  fn: Callable[..., Any],
  mdl: Module,
  *primals,
  has_aux: bool = False,
  reduce_axes=(),
  variables: CollectionFilter = True,
  rngs: PRNGSequenceFilter = True,
):
  """A limited, lifted equivalent of ``jax.value_and_grad``.

  Note that for this convenience function, gradients are only calculated for
  the function inputs, and not with respect to any module variables. The
  target function must return a scalar-valued output.  For a more general
  lifted vjp, see ``nn.vjp`` for the lifted vector-Jacobian product.

  Example::

    class LearnScale(nn.Module):
      @nn.compact
      def __call__(self, x, y):
        p = self.param('scale', nn.initializers.zeros_init(), ())
        return p * x * y

    class Foo(nn.Module):
      @nn.compact
      def __call__(self, x, y):
        z, (x_grad, y_grad) = nn.value_and_grad(
            lambda mdl, x, y: mdl(x, y), LearnScale(), x, y)
        return z, x_grad, y_grad

  Args:
    fn: Function to be differentiated. Its arguments should be arrays, scalars,
      or standard Python containers of arrays or scalars. It should return an
      array, scalar, or standard Python container of arrays or scalars. It will
      receive the scope and primals as arguments.
    mdl: The module of which the variables will be differentiated.
    *primals: A sequence of primal values at which the Jacobian of ``fn``
      should be evaluated. The length of ``primals`` should be equal to the
      number of positional parameters to ``fn``. Each primal value should be a
      tuple of arrays, scalar, or standard Python containers thereof.
    has_aux: Optional, bool. Indicates whether ``fn`` returns a pair where the
     first element is considered the output of the mathematical function to be
     differentiated and the second element is auxiliary data. Default ``False``.
    variables: variables collections that are available inside ``fn`` but
      do not receive a cotangent.
    rngs: the prngs that are available inside ``fn``.
  Returns:
    If ``has_aux`` is ``False``, returns a ``primals_out, grads`` pair, where
    ``primals_out`` is ``fn(*primals)``.  ``grads`` are the gradients for the
    corresponding primals and do not include the gradients for module variables.
    If ``has_aux`` is ``True``, returns a
    ``(primals_out, aux), grads`` tuple where ``aux`` is the auxiliary data
    returned by ``fn``.
  """
  if reduce_axes:
    raise NotImplementedError(
        'reduce_axes argument to value_and_grad is deprecated')
  del reduce_axes

  grad_partial = functools.partial(
    lift_direct_transform,
    lift.value_and_grad,
    (fn,),
    mdl,
    *primals,
    has_aux=has_aux,
    variables=variables,
    rngs=rngs,
  )

  if has_aux:
    out, aux, argument_grads = grad_partial()
    if out.shape != ():
      raise ValueError(
        'grad can only work on functions with '
        f'scalar-valued outputs. out shape={out.shape}'
      )
    return (out, aux), argument_grads
  else:
    out, argument_grads = grad_partial()
    if out.shape != ():
      raise ValueError(
        'grad can only work on functions with '
        f'scalar-valued outputs. out shape={out.shape}'
      )
    return out, argument_grads


def value_and_grad(
  f: tp.Callable[..., tp.Any],
  *,
  argnums: int | DiffState | tp.Sequence[int | DiffState] = 0,
  has_aux: bool = False,
  holomorphic: bool = False,
  allow_int: bool = False,
  reduce_axes: tp.Sequence[AxisName] = (),
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> tp.Callable[..., tp.Any]: ...


def value_and_grad(
  *,
  argnums: int | DiffState | tp.Sequence[int | DiffState] = 0,
  has_aux: bool = False,
  holomorphic: bool = False,
  allow_int: bool = False,
  reduce_axes: tp.Sequence[AxisName] = (),
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> tp.Callable[[tp.Callable[..., tp.Any]], tp.Callable[..., tp.Any]]: ...


def value_and_grad(
  f: tp.Callable[..., tp.Any] | type[Missing] = Missing,
  *,
  argnums: int | DiffState | tp.Sequence[int | DiffState] = 0,
  has_aux: bool = False,
  holomorphic: bool = False,
  allow_int: bool = False,
  reduce_axes: tp.Sequence[AxisName] = (),
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> (
  tp.Callable[..., tp.Any]
  | tp.Callable[[tp.Callable[..., tp.Any]], tp.Callable[..., tp.Any]]
):
  """Object-aware version of ``jax.value_and_grad``.

  Like :func:`grad`, but returns both the value and the gradient of ``f``.

  Args:
    f: Function to be differentiated. Its arguments at positions specified by
      ``argnums`` should be arrays, scalars, graph nodes or standard Python
      containers. Argument arrays in the positions specified by ``argnums`` must
      be of inexact (i.e., floating-point or complex) type. It should return a
      scalar (which includes arrays with shape ``()`` but not arrays with shape
      ``(1,)`` etc.)
    argnums: Optional, integer or sequence of integers. Specifies which
      positional argument(s) to differentiate with respect to (default 0).
    has_aux: Optional, bool. Indicates whether ``f`` returns a pair where the
      first element is considered the output of the mathematical function to be
      differentiated and the second element is auxiliary data. Default False.
    holomorphic: Optional, bool. Indicates whether ``f`` is promised to be
      holomorphic. If True, inputs and outputs must be complex. Default False.
    allow_int: Optional, bool. Whether to allow differentiating with
      respect to integer valued inputs. The gradient of an integer input will
      have a trivial vector-space dtype (float0). Default False.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references and reference semantics.
      If ``False``, uses tree-mode which treats Modules as regular JAX
      pytrees, avoiding the overhead of the graph protocol. Tree-mode does
      not support ``DiffState`` or shared ``Variable`` references.
    graph_updates: If ``True``, propagates updates on graph structure
      that happen inside the transform to the input graphs, has no
      effect when ``graph=False``. When ``False``, using ``DiffState``
      is not supported.

  Returns:
    A function with the same arguments as ``f`` that evaluates both ``f``
    and the gradient of ``f`` and returns them as a pair (a two-element
    tuple). If ``argnums`` is an integer then the gradient has the same shape
    and type as the positional argument indicated by that integer. If argnums is
    a sequence of integers, the gradient is a tuple of values with the same
    shapes and types as the corresponding arguments. If ``has_aux`` is True
    then a tuple of ((value, auxiliary_data), gradient) is returned.
  """
  if graph is None:
    graph = graphlib.set_graph_mode.current_value()
  if graph_updates is None:
    graph_updates = graphlib.set_graph_updates.current_value()
  if reduce_axes:
    raise NotImplementedError(
        'reduce_axes argument to value_and_grad is deprecated')
  del reduce_axes

  if f is Missing:
    return functools.partial(
      value_and_grad,
      argnums=argnums,
      has_aux=has_aux,
      holomorphic=holomorphic,
      allow_int=allow_int,
      graph=graph,
      graph_updates=graph_updates,
    )
  # Detect bound nnx.Module methods and raise error.
  f_unbound, _, was_bound = _resolve_bound_callable(f)

  if was_bound:
    _raise_bound_method_error('value_and_grad')

  return _grad_general(
    f_unbound,
    argnums,
    has_aux,
    holomorphic,
    allow_int,
    return_value=True,
    graph=graph,
    graph_updates=graph_updates,
  )

