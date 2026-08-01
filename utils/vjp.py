
def vjp(func, inputs, v=None, create_graph=False, strict=False):
    r"""Compute the dot product between a vector ``v`` and the Jacobian of the given function at the point given by the inputs.

    Args:
        func (function): a Python function that takes Tensor inputs and returns
            a tuple of Tensors or a Tensor.
        inputs (tuple of Tensors or Tensor): inputs to the function ``func``.
        v (tuple of Tensors or Tensor): The vector for which the vector
            Jacobian product is computed.  Must be the same size as the output
            of ``func``. This argument is optional when the output of ``func``
            contains a single element and (if it is not provided) will be set
            as a Tensor containing a single ``1``.
        create_graph (bool, optional): If ``True``, both the output and result
            will be computed in a differentiable way. Note that when ``strict``
            is ``False``, the result can not require gradients or be
            disconnected from the inputs.  Defaults to ``False``.
        strict (bool, optional): If ``True``, an error will be raised when we
            detect that there exists an input such that all the outputs are
            independent of it. If ``False``, we return a Tensor of zeros as the
            vjp for said inputs, which is the expected mathematical value.
            Defaults to ``False``.

    Returns:
        output (tuple): tuple with:
            func_output (tuple of Tensors or Tensor): output of ``func(inputs)``

            vjp (tuple of Tensors or Tensor): result of the dot product with
            the same shape as the inputs.

    Example:

        >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_AUTOGRAD)
        >>> def exp_reducer(x):
        ...     return x.exp().sum(dim=1)
        >>> inputs = torch.rand(4, 4)
        >>> v = torch.ones(4)
        >>> # xdoctest: +IGNORE_WANT("non-deterministic")
        >>> vjp(exp_reducer, inputs, v)
        (tensor([5.7817, 7.2458, 5.7830, 6.7782]),
         tensor([[1.4458, 1.3962, 1.3042, 1.6354],
                [2.1288, 1.0652, 1.5483, 2.5035],
                [2.2046, 1.1292, 1.1432, 1.3059],
                [1.3225, 1.6652, 1.7753, 2.0152]]))

        >>> vjp(exp_reducer, inputs, v, create_graph=True)
        (tensor([5.7817, 7.2458, 5.7830, 6.7782], grad_fn=<SumBackward1>),
         tensor([[1.4458, 1.3962, 1.3042, 1.6354],
                [2.1288, 1.0652, 1.5483, 2.5035],
                [2.2046, 1.1292, 1.1432, 1.3059],
                [1.3225, 1.6652, 1.7753, 2.0152]], grad_fn=<MulBackward0>))

        >>> def adder(x, y):
        ...     return 2 * x + 3 * y
        >>> inputs = (torch.rand(2), torch.rand(2))
        >>> v = torch.ones(2)
        >>> vjp(adder, inputs, v)
        (tensor([2.4225, 2.3340]),
         (tensor([2., 2.]), tensor([3., 3.])))
    """
    with torch.enable_grad():
        is_inputs_tuple, inputs = _as_tuple(inputs, "inputs", "vjp")
        inputs = _grad_preprocess(inputs, create_graph=create_graph, need_graph=True)

        outputs = func(*inputs)
        is_outputs_tuple, outputs = _as_tuple(
            outputs, "outputs of the user-provided function", "vjp"
        )
        _check_requires_grad(outputs, "outputs", strict=strict)

        if v is not None:
            _, v = _as_tuple(v, "v", "vjp")
            v = _grad_preprocess(v, create_graph=create_graph, need_graph=False)
            _validate_v(v, outputs, is_outputs_tuple)
        else:
            if len(outputs) != 1 or outputs[0].nelement() != 1:
                raise RuntimeError(
                    "The vector v can only be None if the "
                    "user-provided function returns "
                    "a single Tensor with a single element."
                )

    enable_grad = True if create_graph else torch.is_grad_enabled()
    with torch.set_grad_enabled(enable_grad):
        grad_res = _autograd_grad(outputs, inputs, v, create_graph=create_graph)
        vjp = _fill_in_zeros(grad_res, inputs, strict, create_graph, "back")

    # Cleanup objects and return them to the user
    outputs = _grad_postprocess(outputs, create_graph)
    vjp = _grad_postprocess(vjp, create_graph)

    return _tuple_postprocess(outputs, is_outputs_tuple), _tuple_postprocess(
        vjp, is_inputs_tuple
    )


def vjp(func: Callable[..., Any], *primals: Any, has_aux: bool = False) -> Any:
    warn_deprecated("vjp")
    return _impl.vjp(func, *primals, has_aux=has_aux)


def vjp(
    func: Callable[..., Any], *primals: Any, has_aux: bool = False
) -> tuple[Any, Callable[..., Any]] | tuple[Any, Callable[..., Any], Any]:
    """
    Standing for the vector-Jacobian product, returns a tuple containing the
    results of ``func`` applied to ``primals`` and a function that, when
    given ``cotangents``, computes the reverse-mode Jacobian of ``func`` with
    respect to ``primals`` times ``cotangents``.

    Args:
        func (Callable[..., Any]): A Python function that takes one or more arguments. Must
            return one or more Tensors.
        primals (Tensors): Positional arguments to ``func`` that must all be
            Tensors. The returned function will also be computing the
            derivative with respect to these arguments
        has_aux (bool): Flag indicating that ``func`` returns a
            ``(output, aux)`` tuple where the first element is the output of
            the function to be differentiated and the second element is
            other auxiliary objects that will not be differentiated.
            Default: False.

    Returns:
        Returns a ``(output, vjp_fn)`` tuple containing the output of ``func``
        applied to ``primals`` and a function that computes the vjp of
        ``func`` with respect to all ``primals`` using the cotangents passed
        to the returned function. If ``has_aux is True``, then instead returns a
        ``(output, vjp_fn, aux)`` tuple.
        The returned ``vjp_fn`` function will return a tuple of each VJP.

    When used in simple cases, :func:`vjp` behaves the same as :func:`grad`

        >>> x = torch.randn([5])
        >>> f = lambda x: x.sin().sum()
        >>> (_, vjpfunc) = torch.func.vjp(f, x)
        >>> grad = vjpfunc(torch.tensor(1.0))[0]
        >>> assert torch.allclose(grad, torch.func.grad(f)(x))

    However, :func:`vjp` can support functions with multiple outputs by
    passing in the cotangents for each of the outputs

        >>> x = torch.randn([5])
        >>> f = lambda x: (x.sin(), x.cos())
        >>> (_, vjpfunc) = torch.func.vjp(f, x)
        >>> vjps = vjpfunc((torch.ones([5]), torch.ones([5])))
        >>> assert torch.allclose(vjps[0], x.cos() + -x.sin())

    :func:`vjp` can even support outputs being Python structs

        >>> x = torch.randn([5])
        >>> f = lambda x: {"first": x.sin(), "second": x.cos()}
        >>> (_, vjpfunc) = torch.func.vjp(f, x)
        >>> cotangents = {"first": torch.ones([5]), "second": torch.ones([5])}
        >>> vjps = vjpfunc(cotangents)
        >>> assert torch.allclose(vjps[0], x.cos() + -x.sin())

    The function returned by :func:`vjp` will compute the partials with
    respect to each of the ``primals``

        >>> x, y = torch.randn([5, 4]), torch.randn([4, 5])
        >>> (_, vjpfunc) = torch.func.vjp(torch.matmul, x, y)
        >>> cotangents = torch.randn([5, 5])
        >>> vjps = vjpfunc(cotangents)
        >>> assert len(vjps) == 2
        >>> assert torch.allclose(vjps[0], torch.matmul(cotangents, y.transpose(0, 1)))
        >>> assert torch.allclose(vjps[1], torch.matmul(x.transpose(0, 1), cotangents))

    ``primals`` are the positional arguments for ``f``. All kwargs use their
    default value

        >>> x = torch.randn([5])
        >>> def f(x, scale=4.):
        >>>   return x * scale
        >>>
        >>> (_, vjpfunc) = torch.func.vjp(f, x)
        >>> vjps = vjpfunc(torch.ones_like(x))
        >>> assert torch.allclose(vjps[0], torch.full(x.shape, 4.0))

    .. note::
        Using PyTorch ``torch.no_grad`` together with ``vjp``.
        Case 1: Using ``torch.no_grad`` inside a function:

            >>> def f(x):
            >>>     with torch.no_grad():
            >>>         c = x ** 2
            >>>     return x - c

        In this case, ``vjp(f)(x)`` will respect the inner ``torch.no_grad``.

        Case 2: Using ``vjp`` inside ``torch.no_grad`` context manager:

            >>> # xdoctest: +SKIP(failing)
            >>> with torch.no_grad():
            >>>     vjp(f)(x)

        In this case, ``vjp`` will respect the inner ``torch.no_grad``, but not the
        outer one. This is because ``vjp`` is a "function transform": its result
        should not depend on the result of a context manager outside of ``f``.
    """
    return _vjp_with_argnums(func, *primals, has_aux=has_aux)


def vjp(fun: Callable[..., T],
        *primals: Any,
        has_aux: Literal[False] = False,
        reduce_axes: Sequence[AxisName] = ()) -> tuple[T, Callable]:
  ...


def vjp(fun: Callable[..., tuple[T, U]], *primals: Any,
        has_aux: Literal[True],
        reduce_axes: Sequence[AxisName] = ()) -> tuple[T, Callable, U]:
  ...


def vjp(
    fun: Callable, *primals, has_aux: bool = False, reduce_axes=()
  ) -> tuple[Any, Callable] | tuple[Any, Callable, Any]:
  """Compute a (reverse-mode) vector-Jacobian product of ``fun``.

  :py:func:`grad` is implemented as a special case of :py:func:`vjp`.

  Args:
    fun: Function to be differentiated. Its arguments should be arrays, scalars,
      or standard Python containers of arrays or scalars. It should return an
      array, scalar, or standard Python container of arrays or scalars.
    primals: A sequence of primal values at which the Jacobian of ``fun``
      should be evaluated. The number of ``primals`` should be equal to the
      number of positional parameters of ``fun``. Each primal value should be
      an array, a scalar, or a pytree (standard Python containers) thereof.
    has_aux: Optional, bool. Indicates whether ``fun`` returns a pair where the
     first element is considered the output of the mathematical function to be
     differentiated and the second element is auxiliary data. Default False.

  Returns:
    If ``has_aux`` is ``False``, returns a ``(primals_out, vjpfun)`` pair, where
    ``primals_out`` is ``fun(*primals)``. If ``has_aux`` is ``True``, returns a
    ``(primals_out, vjpfun, aux)`` tuple where ``aux`` is the auxiliary data
    returned by ``fun``.

    ``vjpfun`` is a function from a cotangent vector with the same shape as
    ``primals_out`` to a tuple of cotangent vectors with the same number and
    shapes as ``primals``, representing the vector-Jacobian product of ``fun``
    evaluated at ``primals``.

  >>> import jax
  >>>
  >>> def f(x, y):
  ...   return jax.numpy.sin(x), jax.numpy.cos(y)
  ...
  >>> primals, f_vjp = jax.vjp(f, 0.5, 1.0)
  >>> xbar, ybar = f_vjp((-0.7, 0.3))
  >>> print(xbar)
  -0.61430776
  >>> print(ybar)
  -0.2524413
  """
  if reduce_axes:
    raise NotImplementedError("reduce_axes argument to vjp is deprecated")
  del reduce_axes
  check_callable(fun)
  canon = lambda x: x if isinstance(x, core.Tracer) else canonicalize_value(x)
  primals_ft = FlatTree.flatten(primals).map(canon)
  primals_ft.map(dispatch.check_arg)
  out_primals_ft, out_known, jaxpr, residuals, *maybe_aux = ad.linearize(
      fun, primals_ft, is_vjp=True, has_aux=has_aux)

  id_map = {id(x): i for i, x in enumerate(primals_ft)}
  used, opaque_residuals = set(), []
  spec = [used.add(id(r)) or RSpec(id_map[id(r)], True) if id(r) in id_map else
          RSpec(opaque_residuals.append(r) or (len(opaque_residuals) - 1), False)
          for r in residuals]
  args_res = tuptree_map(lambda x: x if id(x) in used else NotNeeded(),
                         primals_ft.tree, list(primals_ft))
  out_primal_avals = list(out_primals_ft.map(typeof))
  f_vjp = VJP(partial(_vjp3_callable, spec, out_known, jaxpr, out_primal_avals),
              primals_ft.tree, out_primals_ft.tree, list(args_res), opaque_residuals)
  return out_primals_ft.unflatten(), f_vjp, *maybe_aux


def vjp(
  fn: Callable[..., Any],
  scope: Scope,
  *primals,
  has_aux: bool = False,
  reduce_axes=(),
  vjp_variables: CollectionFilter = 'params',
  variables: CollectionFilter = True,
  rngs: PRNGSequenceFilter = True,
) -> tuple[Any, Callable[..., Any]] | tuple[Any, Callable[..., Any], Any]:
  """A lifted version of ``jax.vjp``.

  See ``jax.vjp`` for the unlifted vector-Jacobian product (backward gradient).

  Note that a gradient is returned for all variables in the collections
  specified by `vjp_variables`. However, the backward function only expects
  a cotangent for the return value of `fn`. If variables require a co-tangent
  as well they can be returned from `fn` using `scope.variables()`.

  Example::

    def learn_scale(scope, x, y):
      p = scope.param('scale', nn.initializers.zeros_init(), ())
      return p * x * y
    def f(scope, x, y):
      z, bwd = lift.vjp(learn_scale, scope, x, y)
      params_grad, x_grad, y_grad = bwd(jnp.ones(z.shape))
      return z, params_grad, x_grad, y_grad

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
    vjp_variables: The vjpfun will return a cotangent vector for all
      variable collections specified by this filter.
    variables: other variables collections that are available inside `fn` but
      do not receive a cotangent.
    rngs: the prngs that are available inside `fn`.

  Returns:
    If ``has_aux`` is ``False``, returns a ``(primals_out, vjpfun)`` pair, where
    ``primals_out`` is ``fn(*primals)``.
    ``vjpfun`` is a function from a cotangent vector with the same shape as
    ``primals_out`` to a tuple of cotangent vectors with the same shape as
    ``primals``, representing the vector-Jacobian product of ``fn`` evaluated at
    ``primals``. If ``has_aux`` is ``True``, returns a
    ``(primals_out, vjpfun, aux)`` tuple where ``aux`` is the auxiliary data
    returned by ``fn``.
  """
  if reduce_axes:
    raise NotImplementedError('reduce_axes argument to vjp is deprecated')
  del reduce_axes

  def inner(scope_fn, repack_fn, variable_groups, rng_groups, *args):
    vjp_vars, other_vars = variable_groups

    @functools.wraps(fn)
    def wrapper(vjp_vars, *args):
      variable_groups = (vjp_vars, other_vars)
      scope = scope_fn(variable_groups, rng_groups)
      if has_aux:
        y, aux = fn(scope, *args)
      else:
        y = fn(scope, *args)
        aux = ()
      return y, (aux, repack_fn(scope))

    y, bwd, (aux, out_vars) = jax.vjp(
      wrapper, vjp_vars, *args, has_aux=True
    )
    treedef = jax.tree_util.tree_structure(scope)
    bwd = jax.tree_util.Partial(functools.partial(_bwd_wrapper, treedef), bwd)
    if has_aux:
      return (y, bwd, aux), out_vars
    else:
      return (y, bwd), out_vars

  return pack(
    inner,
    (vjp_variables, variables),
    (variables,),
    (rngs,),
    name='vjp',
    enable_kwargs=False,
  )(scope, *primals)


def vjp(
  fn: Callable[..., Any],
  mdl: Module,
  *primals,
  has_aux: bool = False,
  reduce_axes=(),
  vjp_variables: CollectionFilter = 'params',
  variables: CollectionFilter = True,
  rngs: PRNGSequenceFilter = True,
  multi_scope: bool = False,
):
  """A lifted version of ``jax.vjp``.

  See ``jax.vjp`` for the unlifted vector-Jacobian product (backward gradient).

  Note that a gradient is returned for all variables in the collections
  specified by ``vjp_variables``. However, the backward function only expects
  a cotangent for the return value of ``fn``. If variables require a co-tangent
  as well they can be returned from ``fn`` using ``Module.variables``.

  Example::

    >>> import flax.linen as nn
    >>> import jax.numpy as jnp

    >>> class LearnScale(nn.Module):
    ...   @nn.compact
    ...   def __call__(self, x, y):
    ...     p = self.param('scale', nn.initializers.zeros_init(), ())
    ...     return p * x * y

    >>> class Foo(nn.Module):
    ...   @nn.compact
    ...   def __call__(self, x, y):
    ...     z, bwd = nn.vjp(lambda mdl, x, y: mdl(x, y), LearnScale(), x, y)
    ...     params_grad, x_grad, y_grad = bwd(jnp.ones(z.shape))
    ...     return z, params_grad, x_grad, y_grad

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
    vjp_variables: The vjpfun will return a cotangent vector for all
      variable collections specified by this filter.
    variables: other variables collections that are available inside ``fn`` but
      do not receive a cotangent.
    rngs: the prngs that are available inside ``fn``.
    multi_scope: for Modules containing multiple scopes from outside modules passed in,
      allow for variable gradients to be returned for multiple scopes instead of erroring.
  Returns:
    If ``has_aux`` is ``False``, returns a ``(primals_out, vjpfun)`` pair, where
    ``primals_out`` is ``fn(*primals)``.
    ``vjpfun`` is a function from a cotangent vector with the same shape as
    ``primals_out`` to a tuple of cotangent vectors with the same shape as
    ``primals``, representing the vector-Jacobian product of ``fn`` evaluated at
    ``primals``. If ``has_aux`` is ``True``, returns a
    ``(primals_out, vjpfun, aux)`` tuple where ``aux`` is the auxiliary data
    returned by ``fn``.
  """
  if reduce_axes:
    raise NotImplementedError('reduce_axes argument to vjp is deprecated')
  del reduce_axes

  return lift_direct_transform(
    lift.vjp,
    (fn,),
    mdl,
    *primals,
    multi_scope=multi_scope,
    has_aux=has_aux,
    vjp_variables=vjp_variables,
    variables=variables,
    rngs=rngs,
  )


def vjp(
  f: tp.Callable[..., tp.Any],
  *primals: tp.Any,
  has_aux: bool = False,
  reduce_axes: tp.Sequence[AxisName] = (),
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> tuple[tp.Any, tp.Callable] | tuple[tp.Any, tp.Callable, tp.Any]: ...


def vjp(
  *,
  has_aux: bool = False,
  reduce_axes: tp.Sequence[AxisName] = (),
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> tp.Callable[[tp.Callable[..., tp.Any]], tp.Callable[..., tp.Any]]: ...


def vjp(
  f: tp.Callable[..., tp.Any] | Missing = MISSING,
  *primals: tp.Any,
  has_aux: bool = False,
  reduce_axes: tp.Sequence[AxisName] = (),
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> (
  tuple[tp.Any, tp.Callable]
  | tuple[tp.Any, tp.Callable, tp.Any]
  | tp.Callable[[tp.Callable[..., tp.Any]], tp.Callable[..., tp.Any]]
):
  """Stateful version of ``jax.vjp`` that propagates NNX Variable updates.

  Example::

    >>> from flax import nnx
    >>> import jax.numpy as jnp
    ...
    >>> m = nnx.Linear(2, 3, rngs=nnx.Rngs(0))
    >>> x = jnp.ones((1, 2))
    ...
    >>> def loss_fn(m, x):
    ...   return jnp.sum(m(x))
    ...
    >>> primals_out, vjp_fn = nnx.vjp(loss_fn, m, x, graph=False)
    >>> m_grad, x_grad = vjp_fn(jnp.ones_like(primals_out))

  Can also be used as a decorator::

    >>> @nnx.vjp(graph=False)
    ... def f(m, x):
    ...   return jnp.sum(m(x))
    ...
    >>> primals_out, vjp_fn = f(m, x)

  Args:
    f: Function to be differentiated. Its arguments can be arrays, scalars,
      or pytrees containing arrays and NNX Variables.
    *primals: A sequence of primal values at which the Jacobian of ``f``
      should be evaluated.
    has_aux: Optional, bool. Indicates whether ``f`` returns a pair where the
      first element is considered the output of the mathematical function to be
      differentiated and the second element is auxiliary data. Default False.
    reduce_axes: Deprecated, do not use.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references and reference semantics.
      If ``False``, uses tree-mode which treats Modules as regular JAX
      pytrees, avoiding the overhead of the graph protocol.
    graph_updates: If ``True``, propagates updates on graph structure
      that happen inside the transform to the input graphs, has no
      effect when ``graph=False``.

  Returns:
    If ``has_aux`` is False, returns a ``(primals_out, vjp_fn)`` pair.
    ``vjp_fn`` takes a cotangent with the same structure as ``primals_out``
    and returns gradients for each primal argument.
    If ``has_aux`` is True, returns ``(primals_out, vjp_fn, aux)``.
  """
  if graph is None:
    graph = graphlib.set_graph_mode.current_value()
  if graph_updates is None:
    graph_updates = graphlib.set_graph_updates.current_value()
  if graph and graph_updates:
    raise NotImplementedError(
      'graph-mode with graph_updates is not supported for nnx.vjp. '
      'Set graph=False or graph_updates=False.'
    )
  if reduce_axes:
    raise NotImplementedError('reduce_axes argument to vjp is deprecated')
  del reduce_axes

  if isinstance(f, Missing):
    return functools.partial(  # type: ignore[return-value]
      vjp,
      has_aux=has_aux,
      graph=graph,
      graph_updates=graph_updates,
    )

  f_unbound, _, was_bound = _resolve_bound_callable(f)
  if was_bound:
    _raise_bound_method_error('vjp')

  if not primals:
    return functools.partial(  # type: ignore[return-value]
      vjp,
      f,
      has_aux=has_aux,
      graph=graph,
      graph_updates=graph_updates,
    )

  if graph:
    primals = extract.to_tree2(primals)
  extract.check_no_aliases('vjp', primals=primals)
  primals_out, vjp_fn, aux = jax.vjp(
    SimpleVjpFn(f_unbound, has_aux=has_aux, graph=graph),
    *primals,
    has_aux=True,
  )
  if has_aux:
    updates, user_aux = aux
  else:
    updates = aux
    user_aux = None
  if graph:
    primals_out = extract.from_tree2(primals_out)
    raw_vjp_fn = vjp_fn
    def vjp_fn(g):
      return extract.from_tree2(raw_vjp_fn(g))
  extract.apply_variable_updates(primals, updates)
  if has_aux:
    return primals_out, vjp_fn, user_aux
  else:
    return primals_out, vjp_fn

