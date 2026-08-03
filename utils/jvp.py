import functools
from typing import Any, Callable

def jvp(func, inputs, v=None, create_graph=False, strict=False):
    r"""Compute the dot product between the Jacobian of the given function at the point given by the inputs and a vector ``v``.

    Args:
        func (function): a Python function that takes Tensor inputs and returns
            a tuple of Tensors or a Tensor.
        inputs (tuple of Tensors or Tensor): inputs to the function ``func``.
        v (tuple of Tensors or Tensor): The vector for which the Jacobian
            vector product is computed. Must be the same size as the input of
            ``func``. This argument is optional when the input to ``func``
            contains a single element and (if it is not provided) will be set
            as a Tensor containing a single ``1``.
        create_graph (bool, optional): If ``True``, both the output and result
            will be computed in a differentiable way. Note that when ``strict``
            is ``False``, the result can not require gradients or be
            disconnected from the inputs.  Defaults to ``False``.
        strict (bool, optional): If ``True``, an error will be raised when we
            detect that there exists an input such that all the outputs are
            independent of it. If ``False``, we return a Tensor of zeros as the
            jvp for said inputs, which is the expected mathematical value.
            Defaults to ``False``.

    Returns:
        output (tuple): tuple with:
            func_output (tuple of Tensors or Tensor): output of ``func(inputs)``

            jvp (tuple of Tensors or Tensor): result of the dot product with
            the same shape as the output.

    Note:
        ``autograd.functional.jvp`` computes the jvp by using the backward of
        the backward (sometimes called the double backwards trick). This is not
        the most performant way of computing the jvp. Please consider using
        :func:`torch.func.jvp` or the
        :ref:`low-level forward-mode AD API <forward-mode-ad>` instead.

    Example:

        >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_AUTOGRAD)
        >>> def exp_reducer(x):
        ...     return x.exp().sum(dim=1)
        >>> inputs = torch.rand(4, 4)
        >>> v = torch.ones(4, 4)
        >>> # xdoctest: +IGNORE_WANT("non-deterministic")
        >>> jvp(exp_reducer, inputs, v)
        (tensor([6.3090, 4.6742, 7.9114, 8.2106]),
         tensor([6.3090, 4.6742, 7.9114, 8.2106]))

        >>> jvp(exp_reducer, inputs, v, create_graph=True)
        (tensor([6.3090, 4.6742, 7.9114, 8.2106], grad_fn=<SumBackward1>),
         tensor([6.3090, 4.6742, 7.9114, 8.2106], grad_fn=<SqueezeBackward1>))

        >>> def adder(x, y):
        ...     return 2 * x + 3 * y
        >>> inputs = (torch.rand(2), torch.rand(2))
        >>> v = (torch.ones(2), torch.ones(2))
        >>> jvp(adder, inputs, v)
        (tensor([2.2399, 2.5005]),
         tensor([5., 5.]))

    """
    with torch.enable_grad():
        is_inputs_tuple, inputs = _as_tuple(inputs, "inputs", "jvp")
        inputs = _grad_preprocess(inputs, create_graph=create_graph, need_graph=True)

        if v is not None:
            _, v = _as_tuple(v, "v", "jvp")
            v = _grad_preprocess(v, create_graph=create_graph, need_graph=False)
            _validate_v(v, inputs, is_inputs_tuple)
        else:
            if len(inputs) != 1 or inputs[0].nelement() != 1:
                raise RuntimeError(
                    "The vector v can only be None if the input to "
                    "the user-provided function is a single Tensor "
                    "with a single element."
                )

        outputs = func(*inputs)
        is_outputs_tuple, outputs = _as_tuple(
            outputs, "outputs of the user-provided function", "jvp"
        )
        _check_requires_grad(outputs, "outputs", strict=strict)
        # The backward is linear so the value of grad_outputs is not important as
        # it won't appear in the double backward graph. We only need to ensure that
        # it does not contain inf or nan.
        grad_outputs = tuple(
            torch.zeros_like(out, requires_grad=True) for out in outputs
        )

        grad_inputs = _autograd_grad(outputs, inputs, grad_outputs, create_graph=True)
        _check_requires_grad(grad_inputs, "grad_inputs", strict=strict)

    if create_graph:
        with torch.enable_grad():
            grad_res = _autograd_grad(
                grad_inputs, grad_outputs, v, create_graph=create_graph
            )
            jvp = _fill_in_zeros(grad_res, outputs, strict, create_graph, "back_trick")
    else:
        grad_res = _autograd_grad(
            grad_inputs, grad_outputs, v, create_graph=create_graph
        )
        jvp = _fill_in_zeros(grad_res, outputs, strict, create_graph, "back_trick")

    # Cleanup objects and return them to the user
    outputs = _grad_postprocess(outputs, create_graph)
    jvp = _grad_postprocess(jvp, create_graph)

    return _tuple_postprocess(outputs, is_outputs_tuple), _tuple_postprocess(
        jvp, is_outputs_tuple
    )


def jvp(
    func: Callable[..., Any],
    primals: Any,
    tangents: Any,
    *,
    strict: bool = False,
    has_aux: bool = False,
) -> Any:
    warn_deprecated("jvp")
    return _impl.jvp(func, primals, tangents, strict=strict, has_aux=has_aux)


def jvp(
    func: Callable[..., Any],
    primals: Any,
    tangents: Any,
    *,
    strict: bool = False,
    has_aux: bool = False,
) -> tuple[Any, Any] | tuple[Any, Any, Any]:
    """
    Standing for the Jacobian-vector product, returns a tuple containing
    the output of `func(*primals)` and the "Jacobian of ``func`` evaluated at
    ``primals``" times ``tangents``. This is also known as forward-mode autodiff.

    Args:
        func (function): A Python function that takes one or more arguments,
            one of which must be a Tensor, and returns one or more Tensors
        primals (Tensors): Positional arguments to ``func`` that must all be
            Tensors. The returned function will also be computing the
            derivative with respect to these arguments
        tangents (Tensors): The "vector" for which Jacobian-vector-product is
            computed. Must be the same structure and sizes as the inputs to
            ``func``.
        has_aux (bool): Flag indicating that ``func`` returns a
            ``(output, aux)`` tuple where the first element is the output of
            the function to be differentiated and the second element is
            other auxiliary objects that will not be differentiated.
            Default: False.

    Returns:
        Returns a ``(output, jvp_out)`` tuple containing the output of ``func``
        evaluated at ``primals`` and the Jacobian-vector product.
        If ``has_aux is True``, then instead returns a ``(output, jvp_out, aux)`` tuple.

    .. note::
        You may see this API error out with "forward-mode AD not implemented
        for operator X". If so, please file a bug report and we will prioritize it.

    jvp is useful when you wish to compute gradients of a function R^1 -> R^N

        >>> from torch.func import jvp
        >>> x = torch.randn([])
        >>> f = lambda x: x * torch.tensor([1.0, 2.0, 3])
        >>> value, grad = jvp(f, (x,), (torch.tensor(1.0),))
        >>> assert torch.allclose(value, f(x))
        >>> assert torch.allclose(grad, torch.tensor([1.0, 2, 3]))

    :func:`jvp` can support functions with multiple inputs by passing in the
    tangents for each of the inputs

         >>> from torch.func import jvp
         >>> x = torch.randn(5)
         >>> y = torch.randn(5)
         >>> f = lambda x, y: (x * y)
         >>> _, output = jvp(f, (x, y), (torch.ones(5), torch.ones(5)))
         >>> assert torch.allclose(output, x + y)

    """

    return _jvp_with_argnums(
        func, primals, tangents, argnums=None, strict=strict, has_aux=has_aux
    )


def jvp(v, z, n=1):
    """Compute derivatives of Bessel functions of the first kind.

    Compute the nth derivative of the Bessel function `Jv` with
    respect to `z`.

    Parameters
    ----------
    v : array_like or float
        Order of Bessel function
    z : complex
        Argument at which to evaluate the derivative; can be real or
        complex.
    n : int, default 1
        Order of derivative. For 0 returns the Bessel function `jv` itself.

    Returns
    -------
    scalar or ndarray
        Values of the derivative of the Bessel function.

    Notes
    -----
    The derivative is computed using the relation DLFM 10.6.7 [2]_.

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996, chapter 5.
           https://people.sc.fsu.edu/~jburkardt/f77_src/special_functions/special_functions.html

    .. [2] NIST Digital Library of Mathematical Functions.
           https://dlmf.nist.gov/10.6.E7

    Examples
    --------

    Compute the Bessel function of the first kind of order 0 and
    its first two derivatives at 1.

    >>> from scipy.special import jvp
    >>> jvp(0, 1, 0), jvp(0, 1, 1), jvp(0, 1, 2)
    (0.7651976865579666, -0.44005058574493355, -0.3251471008130331)

    Compute the first derivative of the Bessel function of the first
    kind for several orders at 1 by providing an array for `v`.

    >>> jvp([0, 1, 2], 1, 1)
    array([-0.44005059,  0.3251471 ,  0.21024362])

    Compute the first derivative of the Bessel function of the first
    kind of order 0 at several points by providing an array for `z`.

    >>> import numpy as np
    >>> points = np.array([0., 1.5, 3.])
    >>> jvp(0, points, 1)
    array([-0.        , -0.55793651, -0.33905896])

    Plot the Bessel function of the first kind of order 1 and its
    first three derivatives.

    >>> import matplotlib.pyplot as plt
    >>> x = np.linspace(-10, 10, 1000)
    >>> fig, ax = plt.subplots()
    >>> ax.plot(x, jvp(1, x, 0), label=r"$J_1$")
    >>> ax.plot(x, jvp(1, x, 1), label=r"$J_1'$")
    >>> ax.plot(x, jvp(1, x, 2), label=r"$J_1''$")
    >>> ax.plot(x, jvp(1, x, 3), label=r"$J_1'''$")
    >>> plt.legend()
    >>> plt.show()
    """
    n = _nonneg_int_or_fail(n, 'n')
    if n == 0:
        return jv(v, z)
    else:
        return _bessel_diff_formula(v, z, n, jv, -1)


def jvp(
    fun: Callable, primals, tangents, has_aux: bool = False
  ) -> tuple[Any, ...]:
  """Computes a (forward-mode) Jacobian-vector product of ``fun``.

  Args:
    fun: Function to be differentiated. Its arguments should be arrays, scalars,
      or standard Python containers of arrays or scalars. It should return an
      array, scalar, or standard Python container of arrays or scalars.
    primals: The primal values at which the Jacobian of ``fun`` should be
      evaluated. Should be either a tuple or a list of arguments,
      and its length should be equal to the number of positional parameters of
      ``fun``.
    tangents: The tangent vector for which the Jacobian-vector product should be
      evaluated. Should be either a tuple or a list of tangents, with the same
      tree structure and array shapes as ``primals``.
    has_aux: Optional, bool. Indicates whether ``fun`` returns a pair where the
     first element is considered the output of the mathematical function to be
     differentiated and the second element is auxiliary data. Default False.

  Returns:
    If ``has_aux`` is ``False``, returns a ``(primals_out, tangents_out)`` pair,
    where ``primals_out`` is ``fun(*primals)``,
    and ``tangents_out`` is the Jacobian-vector product of
    ``function`` evaluated at ``primals`` with ``tangents``. The
    ``tangents_out`` value has the same Python tree structure and shapes as
    ``primals_out``. If ``has_aux`` is ``True``, returns a
    ``(primals_out, tangents_out, aux)`` tuple where ``aux``
    is the auxiliary data returned by ``fun``.

  For example:

  >>> import jax
  >>>
  >>> primals, tangents = jax.jvp(jax.numpy.sin, (0.1,), (0.2,))
  >>> print(primals)
  0.09983342
  >>> print(tangents)
  0.19900084
  """
  check_callable(fun)
  if (not isinstance(primals, (tuple, list)) or
      not isinstance(tangents, (tuple, list))):
    raise TypeError("primal and tangent arguments to jax.jvp must be tuples or lists; "
                    f"found {type(primals).__name__} and {type(tangents).__name__}.")
  return _jvp(fun, primals, tangents, has_aux=has_aux)


def jvp(fun: Callable, primals, tangents, has_aux=False, instantiate=True,
        transform_stack=True) -> Any:
  ctx = (source_info_util.transform_name_stack('jvp') if transform_stack
         else contextlib.nullcontext())
  with core.take_current_trace() as parent_trace:
    tag = core.TraceTag()
    trace = JVPTrace(parent_trace, tag)
    tangents = tangents.map(lambda t:
        p2tz(t) if not isinstance(t, Zero)
        and isinstance(typeof(t), core.ShapedArray)
        and dtype(t) == float0 else t)
    in_tracers = primals.map2(lambda x, t: maybe_jvp_tracer(trace, x, t), tangents)
    with core.set_current_trace(trace), ctx:
      ans = fun(*in_tracers.unflatten())
    if has_aux:
      ans, aux = ans
      auxs = ft.flatten(aux).map(partial(_strip_tracer, JVPTracer, tag)),
    else:
      auxs = ()

    ans_ft = ft.flatten(ans).map(trace.to_primal_tangent_pair)
    out_primals = ans_ft.map(lambda pt: pt[0])
    out_tangents = ans_ft.map(lambda pt: pt[1])

  if type(instantiate) is bool:
    instantiate = [instantiate] * len(out_tangents)
  out_tangents = out_tangents.map2(
      lambda t, inst: instantiate_zeros(t) if inst else t, instantiate
  )
  auxs = tuple(aux.unflatten() for aux in auxs)
  return out_primals, out_tangents, *auxs


def jvp(
  fn: Callable[..., Any],
  scope: Scope,
  primals,
  tangents,
  variable_tangents,
  variables: CollectionFilter = True,
  rngs: PRNGSequenceFilter = True,
) -> tuple[Any, Any]:
  """A lifted version of ``jax.jvp``.

  See ``jax.jvp`` for the unlifted Jacobian-vector product (forward gradient).

  Note that no tangents are returned for variables. When variable tangents
  are required their value should be returned explicitly by `fn`
  using `scope.variables()`.

  Example::

    def learn_scale(scope, x):
      p = scope.param('scale', nn.initializers.zeros_init(), ())
      return p * x

    def f(scope, x):
      vars_t = jax.tree_util.tree_map(jnp.ones_like,
                                      scope.variables().get('params', {}))
      x, out_t = lift.jvp(
          learn_scale, scope, (x,), (jnp.zeros_like(x),),
          variable_tangents={'params': vars_t})
      return out_t

  Args:
    fn: The function to be transformed.
    scope: The scope(s) which should be lifted into the transform.
    primals: The primal values at which the Jacobian of ``fun`` should be
      evaluated. Should be either a tuple or a list of arguments,
      and its length should be equal to the number of positional parameters of
      ``fun``.
    tangents: The tangent vector for which the Jacobian-vector product should be
      evaluated. Should be either a tuple or a list of tangents, with the same
      tree structure and array shapes as ``primals``.
    variable_tangents: A dict or PyTree fo dicts with the same structure as
      scopes. Each entry in the dict specifies the tangents for a variable
      collection. Not specifying a collection in variable_tangents is
      equivalent to passing a zero vector as the tangent.
    variables: other variables collections that are available inside `fn` but
      do not receive a tangent.
    rngs: the prngs that are available inside `fn`.

  Returns:
    A ``(primals_out, tangents_out)`` pair, where ``primals_out`` is
    ``fun(*primals)``, and ``tangents_out`` is the Jacobian-vector product of
    ``function`` evaluated at ``primals`` with ``tangents``. The
    ``tangents_out`` value has the same Python tree structure and shapes as
    ``primals_out``.
  """

  def inner(scope_fn, repack_fn, variable_groups, rng_groups, *args):
    jvp_vars, other_vars = variable_groups

    @functools.wraps(fn)
    def wrapper(vars_primals, args):
      variable_groups = (vars_primals, other_vars)
      scope = scope_fn(variable_groups, rng_groups)
      y = fn(scope, *args)
      return y, repack_fn(scope)

    (y, out_vars), out_tangents = jax.jvp(
      wrapper, (jvp_vars, args), (variable_tangents, tangents)
    )
    return (y, out_tangents[0]), out_vars

  # filter out empty tangent collections because JAX will error on non-equal
  # tree structure for example: {"params": {}} != {}.
  treedef = jax.tree_util.tree_structure(scope)

  variable_tangents = tuple(
    {k: v for k, v in vt.items() if v}  # pylint: disable=g-complex-comprehension
    for vt in treedef.flatten_up_to(variable_tangents)
  )
  target = tuple(variable_tangents[0].keys())
  return pack(
    inner,
    (target, variables),
    (variables,),
    (rngs,),
    name='jvp',
    enable_kwargs=False,
  )(scope, *primals)


def jvp(
  fn: Callable[..., Any],
  mdl: Module,
  primals,
  tangents,
  variable_tangents,
  variables: CollectionFilter = True,
  rngs: PRNGSequenceFilter = True,
) -> tuple[Any, Callable[..., Any]] | tuple[Any, Callable[..., Any], Any]:
  """A lifted version of ``jax.jvp``.

  See ``jax.jvp`` for the unlifted Jacobian-vector product (forward gradient).

  Note that no tangents are returned for variables. When variable tangents
  are required their value should be returned explicitly by ``fn``
  using ``Module.variables``::

    >>> import flax.linen as nn
    >>> import jax.numpy as jnp

    >>> class LearnScale(nn.Module):
    ...   @nn.compact
    ...   def __call__(self, x):
    ...     p = self.param('test', nn.initializers._init(), ())
    ...     return p * x

    >>> class Foo(nn.Module):
    ...   @nn.compact
    ...   def __call__(self, x):
    ...     scale = LearnScale()
    ...     vars_t = jax.tree_util.tree_map(jnp.ones_like,
    ...                                     scale.variables.get('params', {}))
    ...     _, out_t = nn.jvp(
    ...         lambda mdl, x: mdl(x), scale, (x,), (jnp.zeros_like(x),),
    ...         variable_tangents={'params': vars_t})
    ...     return out_t

  Example::

    >>> def learn_scale(scope, x):
    ...   p = scope.param('scale', nn.initializers.zeros_init(), ())
    ...   return p * x

    >>> def f(scope, x):
    ...   vars_t = jax.tree_util.tree_map(jnp.ones_like, scope.variables().get('params', {}))
    ...   x, out_t = lift.jvp(
    ...       learn_scale, scope, (x,), (jnp.zeros_like(x),),
    ...       variable_tangents={'params': vars_t})
    ...   return out_t

  Args:
    fn: Function to be differentiated. Its arguments should be arrays, scalars,
      or standard Python containers of arrays or scalars. It should return an
      array, scalar, or standard Python container of arrays or scalars. It will
      receive the scope and primals as arguments.
    mdl: The module of which the variables will be differentiated.
    primals: The primal values at which the Jacobian of ``fun`` should be
      evaluated. Should be either a tuple or a list of arguments,
      and its length should be equal to the number of positional parameters of
      ``fun``.
    tangents: The tangent vector for which the Jacobian-vector product should be
      evaluated. Should be either a tuple or a list of tangents, with the same
      tree structure and array shapes as ``primals``.
    variable_tangents: A dict or PyTree fo dicts with the same structure as
      scopes. Each entry in the dict specifies the tangents for a variable
      collection. Not specifying a collection in variable_tangents is
      equivalent to passing a zero vector as the tangent.
    variables: other variables collections that are available in ``fn`` but
      do not receive a tangent.
    rngs: the prngs that are available inside ``fn``.

  Returns:
    A ``(primals_out, tangents_out)`` pair, where ``primals_out`` is
    ``fun(*primals)``, and ``tangents_out`` is the Jacobian-vector product of
    ``function`` evaluated at ``primals`` with ``tangents``. The
    ``tangents_out`` value has the same Python tree structure and shapes as
    ``primals_out``.
  """
  return lift_direct_transform(
    lift.jvp,
    (fn,),
    mdl,
    primals,
    tangents,
    variable_tangents,
    multi_scope=False,
    variables=variables,
    rngs=rngs,
  )


def jvp(
  f: tp.Callable[..., tp.Any],
  primals: tuple[tp.Any, ...],
  tangents: tuple[tp.Any, ...],
  *,
  has_aux: bool = False,
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> tuple[tp.Any, ...]: ...


def jvp(
  *,
  has_aux: bool = False,
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> tp.Callable[[tp.Callable[..., tp.Any]], tp.Callable[..., tp.Any]]: ...


def jvp(
  f: tp.Callable[..., tp.Any],
  *,
  has_aux: bool = False,
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> tp.Callable[..., tp.Any]: ...


def jvp(
  f: tp.Callable[..., tp.Any] | Missing = MISSING,
  primals: tuple[tp.Any, ...] | Missing = MISSING,
  tangents: tuple[tp.Any, ...] | Missing = MISSING,
  *,
  has_aux: bool = False,
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> (
  tuple[tp.Any, ...]
  | tp.Callable[..., tp.Any]
  | tp.Callable[[tp.Callable[..., tp.Any]], tp.Callable[..., tp.Any]]
):
  """Stateful version of ``jax.jvp`` that propagates NNX Variable updates.

  Example::

    >>> from flax import nnx
    >>> import jax.numpy as jnp
    ...
    >>> m = nnx.Linear(2, 3, rngs=nnx.Rngs(0))
    >>> x = jnp.ones((1, 2))
    ...
    >>> def f(m, x):
    ...   return jnp.sum(m(x))
    ...
    >>> m_tangent = jax.tree.map(jnp.zeros_like, m)
    >>> x_tangent = jnp.ones_like(x)
    >>> primals_out, tangent_out = nnx.jvp(
    ...   f, (m, x), (m_tangent, x_tangent), graph=False
    ... )

  Can also be used as a decorator::

    >>> @nnx.jvp(graph=False)
    ... def f(m, x):
    ...   return jnp.sum(m(x))
    ...
    >>> primals_out, tangent_out = f((m, x), (m_tangent, x_tangent))

  Args:
    f: Function to be differentiated. Its arguments can be arrays, scalars,
      or pytrees containing arrays and NNX Variables.
    primals: A tuple of primal values at which the Jacobian of ``f``
      should be evaluated.
    tangents: A tuple of tangent vectors, with the same structure as
      ``primals``.
    has_aux: Optional, bool. Indicates whether ``f`` returns a pair where the
      first element is considered the output of the mathematical function to be
      differentiated and the second element is auxiliary data. Default False.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references and reference semantics.
      If ``False``, uses tree-mode which treats Modules as regular JAX
      pytrees, avoiding the overhead of the graph protocol.
    graph_updates: If ``True``, propagates updates on graph structure
      that happen inside the transform to the input graphs, has no
      effect when ``graph=False``.

  Returns:
    If ``has_aux`` is False, returns ``(primals_out, tangent_out)``.
    If ``has_aux`` is True, returns ``(primals_out, tangent_out, aux)``.
  """
  if graph is None:
    graph = graphlib.set_graph_mode.current_value()
  if graph_updates is None:
    graph_updates = graphlib.set_graph_updates.current_value()
  if graph and graph_updates:
    raise NotImplementedError(
      'graph-mode with graph_updates is not supported for nnx.jvp. '
      'Set graph=False or graph_updates=False.'
    )

  if isinstance(f, Missing):
    return functools.partial(
      jvp,
      has_aux=has_aux,
      graph=graph,
      graph_updates=graph_updates,
    )

  f_unbound, _, was_bound = _resolve_bound_callable(f)
  if was_bound:
    _raise_bound_method_error('jvp')

  if isinstance(primals, Missing) or isinstance(tangents, Missing):
    return functools.partial(
      jvp,
      f,
      has_aux=has_aux,
      graph=graph,
      graph_updates=graph_updates,
    )

  if graph:
    primals = extract.to_tree2(primals)
    tangents = extract.to_tree2(tangents)
  extract.check_no_aliases('jvp', primals=primals)
  extract.check_no_aliases('jvp', tangents=tangents)
  if has_aux:
    (primals_out, updates), (tangent_out, _updates_tangent), aux = jax.jvp(
      SimpleJvpFn(f_unbound, has_aux=True, graph=graph),
      primals,
      tangents,
      has_aux=True,
    )
  else:
    (primals_out, updates), (tangent_out, _updates_tangent) = jax.jvp(
      SimpleJvpFn(f_unbound, has_aux=False, graph=graph),
      primals,
      tangents,
    )
  if graph:
    primals_out = extract.from_tree2(primals_out)
    tangent_out = extract.from_tree2(tangent_out)
  extract.apply_variable_updates(primals, updates)
  if has_aux:
    return primals_out, tangent_out, aux
  else:
    return primals_out, tangent_out

