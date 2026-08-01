
def grad(
    outputs: _TensorOrTensorsOrGradEdge,
    inputs: _TensorOrTensorsOrGradEdge,
    grad_outputs: _TensorOrOptionalTensors | None = None,
    retain_graph: bool | None = None,
    create_graph: bool = False,
    only_inputs: bool = True,
    allow_unused: bool | None = None,
    is_grads_batched: bool = False,
    materialize_grads: bool = False,
) -> tuple[torch.Tensor, ...]:
    r"""Compute and return the sum of gradients of outputs with respect to the inputs.

    ``grad_outputs`` should be a sequence of length matching ``output``
    containing the "vector" in vector-Jacobian product, usually the pre-computed
    gradients w.r.t. each of the outputs. If an output doesn't require_grad,
    then the gradient can be ``None``).

    .. note::

        If you run any forward ops, create ``grad_outputs``, and/or call ``grad``
        in a user-specified CUDA stream context, see
        :ref:`Stream semantics of backward passes<bwd-cuda-stream-semantics>`.

    .. note::

        ``only_inputs`` argument is deprecated and is ignored now (defaults to ``True``).
        To accumulate gradient for other parts of the graph, please use
        ``torch.autograd.backward``.

    Args:
        outputs (sequence of Tensor or GradientEdge): outputs of the differentiated function.
        inputs (sequence of Tensor or GradientEdge): Inputs w.r.t. which the gradient will be
            returned (and not accumulated into ``.grad``).
        grad_outputs (sequence of [Tensor or None] or Tensor, optional): The "vector" in the
            vector-Jacobian product. Usually gradients w.r.t. each output. None values can be
            specified for scalar Tensors or ones that don't require grad. If a None value would be
            acceptable for all grad_tensors, then this argument is optional. Default: None.
        retain_graph (bool, optional): If ``False``, the graph used to compute the grad
            will be freed. Note that in nearly all cases setting this option to ``True``
            is not needed and often can be worked around in a much more efficient
            way. Defaults to the value of ``create_graph``.
        create_graph (bool, optional): If ``True``, graph of the derivative will
            be constructed, allowing to compute higher order derivative products.
            Default: ``False``.
        allow_unused (Optional[bool], optional): If ``False``, specifying inputs
            that were not used when computing outputs (and therefore their grad is
            always zero) is an error. Defaults to the value of ``materialize_grads``.
        is_grads_batched (bool, optional): If ``True``, the first dimension of each
            tensor in ``grad_outputs`` will be interpreted as the batch dimension.
            Instead of computing a single vector-Jacobian product, we compute a
            batch of vector-Jacobian products for each "vector" in the batch.
            We use the vmap prototype feature as the backend to vectorize calls
            to the autograd engine so that this computation can be performed in a
            single call. This should lead to performance improvements when compared
            to manually looping and performing backward multiple times. Note that
            due to this feature being experimental, there may be performance
            cliffs. Please use ``torch._C._debug_only_display_vmap_fallback_warnings(True)``
            to show any performance warnings and file an issue on github if warnings exist
            for your use case. Defaults to ``False``.
        materialize_grads (bool, optional): If ``True``, set the gradient for unused inputs
            to zero instead of None. This is useful when computing higher-order derivatives.
            If ``materialize_grads`` is ``True`` and ``allow_unused`` is ``False``, an error
            will be raised. Defaults to ``False``.

    """
    if materialize_grads and allow_unused is False:
        raise ValueError(
            "Expected allow_unused to be True or not passed when materialize_grads=True, "
            "but got: allow_unused=False."
        )
    if allow_unused is None:
        allow_unused = materialize_grads
    if is_tensor_like(outputs) or isinstance(outputs, graph.GradientEdge):
        outputs = cast(
            Sequence[torch.Tensor] | Sequence[graph.GradientEdge], (outputs,)
        )
    else:
        # pyrefly: ignore [bad-argument-type]
        outputs = tuple(outputs)
    if is_tensor_like(inputs) or isinstance(inputs, graph.GradientEdge):
        inputs = cast(_TensorOrTensorsOrGradEdge, (inputs,))
    else:
        # pyrefly: ignore [bad-argument-type]
        inputs = tuple(inputs)
    t_outputs = tuple(i for i in outputs if is_tensor_like(i))
    t_inputs = tuple(i for i in inputs if is_tensor_like(i))
    overridable_args = t_outputs + t_inputs
    if has_torch_function(overridable_args):
        return handle_torch_function(
            grad,
            overridable_args,
            outputs,
            inputs,
            grad_outputs=grad_outputs,
            retain_graph=retain_graph,
            create_graph=create_graph,
            only_inputs=only_inputs,
            allow_unused=allow_unused,
            is_grads_batched=is_grads_batched,
            materialize_grads=materialize_grads,
        )

    if not only_inputs:
        warnings.warn(
            "only_inputs argument is deprecated and is ignored now "
            "(defaults to True). To accumulate gradient for other "
            "parts of the graph, please use torch.autograd.backward.",
            FutureWarning,
            stacklevel=2,
        )

    grad_outputs_ = _tensor_or_tensors_to_tuple(grad_outputs, len(outputs))
    grad_outputs_ = _make_grads(
        outputs, grad_outputs_, is_grads_batched=is_grads_batched
    )

    if retain_graph is None:
        retain_graph = create_graph

    # The reason we repeat the same comment several times below is because
    # some Python versions print out the first line of multi-line function
    # calls in the traceback and some print out the last line
    if is_grads_batched:

        def vjp(gO):
            return _engine_run_backward(
                outputs,
                gO,
                retain_graph,
                create_graph,
                inputs,
                allow_unused,
                accumulate_grad=False,
            )

        result = _vmap_internals._vmap(vjp, 0, 0, allow_none_pass_through=True)(
            grad_outputs_
        )
    else:
        result = _engine_run_backward(
            outputs,
            grad_outputs_,
            retain_graph,
            create_graph,
            inputs,
            allow_unused,
            accumulate_grad=False,
        )
    if materialize_grads:
        if any(
            result[i] is None and not is_tensor_like(inputs[i])
            for i in range(len(inputs))
        ):
            raise RuntimeError(
                "materialize_grads cannot be used when the given input is a GradientEdge"
            )
        result = tuple(
            output
            if output is not None
            # pyrefly: ignore [bad-argument-type]
            else torch.zeros_like(input, requires_grad=create_graph)
            for (output, input) in zip(result, inputs)
        )
    return result


def grad(
    func: Callable[_P, Any], argnums: argnums_t = 0, has_aux: bool = False
) -> Callable[_P, Any]:
    """``grad`` operator helps computing gradients of ``func`` with respect to the
    input(s) specified by ``argnums``. This operator can be nested to
    compute higher-order gradients.

    Args:
        func (Callable): A Python function that takes one or more arguments.
            Must return a single-element Tensor. If specified ``has_aux`` equals ``True``,
            function can return a tuple of single-element Tensor and other auxiliary objects:
            ``(output, aux)``.
        argnums (int or Tuple[int]): Specifies arguments to compute gradients with respect to.
            ``argnums`` can be single integer or tuple of integers. Default: 0.
        has_aux (bool): Flag indicating that ``func`` returns a tensor and other
            auxiliary objects: ``(output, aux)``. Default: False.

    Returns:
        Function to compute gradients with respect to its inputs. By default, the output of
        the function is the gradient tensor(s) with respect to the first argument.
        If specified ``has_aux`` equals ``True``, tuple of gradients and output auxiliary objects
        is returned. If ``argnums`` is a tuple of integers, a tuple of output gradients with
        respect to each ``argnums`` value is returned.

    Example of using ``grad``:

        >>> # xdoctest: +SKIP
        >>> from torch.func import grad
        >>> x = torch.randn([])
        >>> cos_x = grad(lambda x: torch.sin(x))(x)
        >>> assert torch.allclose(cos_x, x.cos())
        >>>
        >>> # Second-order gradients
        >>> neg_sin_x = grad(grad(lambda x: torch.sin(x)))(x)
        >>> assert torch.allclose(neg_sin_x, -x.sin())

    When composed with ``vmap``, ``grad`` can be used to compute per-sample-gradients:

        >>> # xdoctest: +SKIP
        >>> from torch.func import grad, vmap
        >>> batch_size, feature_size = 3, 5
        >>>
        >>> def model(weights, feature_vec):
        >>> # Very simple linear model with activation
        >>>     assert feature_vec.dim() == 1
        >>>     return feature_vec.dot(weights).relu()
        >>>
        >>> def compute_loss(weights, example, target):
        >>>     y = model(weights, example)
        >>>     return ((y - target) ** 2).mean()  # MSELoss
        >>>
        >>> weights = torch.randn(feature_size, requires_grad=True)
        >>> examples = torch.randn(batch_size, feature_size)
        >>> targets = torch.randn(batch_size)
        >>> inputs = (weights, examples, targets)
        >>> grad_weight_per_example = vmap(grad(compute_loss), in_dims=(None, 0, 0))(
        ...     *inputs
        ... )

    Example of using ``grad`` with ``has_aux`` and ``argnums``:

        >>> # xdoctest: +SKIP
        >>> from torch.func import grad
        >>> def my_loss_func(y, y_pred):
        >>>    loss_per_sample = (0.5 * y_pred - y) ** 2
        >>>    loss = loss_per_sample.mean()
        >>>    return loss, (y_pred, loss_per_sample)
        >>>
        >>> fn = grad(my_loss_func, argnums=(0, 1), has_aux=True)
        >>> y_true = torch.rand(4)
        >>> y_preds = torch.rand(4, requires_grad=True)
        >>> out = fn(y_true, y_preds)
        >>> # > output is ((grads w.r.t y_true, grads w.r.t y_preds), (y_pred, loss_per_sample))

    .. note::
        Using PyTorch ``torch.no_grad`` together with ``grad``.

        Case 1: Using ``torch.no_grad`` inside a function:

            >>> # xdoctest: +SKIP
            >>> def f(x):
            >>>     with torch.no_grad():
            >>>         c = x ** 2
            >>>     return x - c

        In this case, ``grad(f)(x)`` will respect the inner ``torch.no_grad``.

        Case 2: Using ``grad`` inside ``torch.no_grad`` context manager:

            >>> # xdoctest: +SKIP
            >>> with torch.no_grad():
            >>>     grad(f)(x)

        In this case, ``grad`` will respect the inner ``torch.no_grad``, but not the
        outer one. This is because ``grad`` is a "function transform": its result
        should not depend on the result of a context manager outside of ``f``.

    """
    # To avoid cyclical dependency.
    import torch._functorch.eager_transforms as eager_transforms
    from torch.compiler import is_compiling

    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> tuple[Any, torch.Tensor]:
        return eager_transforms.grad_impl(func, argnums, has_aux, args, kwargs)

    if not is_compiling():
        wrapper = functools.wraps(func)(wrapper)

    return wrapper


def grad(
    func: Callable[..., Any], argnums: argnums_t = 0, has_aux: bool = False
) -> Callable[..., Any]:
    warn_deprecated("grad")
    return apis.grad(func, argnums, has_aux)


def grad(fun: Callable, argnums: int | Sequence[int] = 0,
         has_aux: bool = False, holomorphic: bool = False,
         allow_int: bool = False,
         reduce_axes: Sequence[AxisName] = ()) -> Callable:
  """Creates a function that evaluates the gradient of ``fun``.

  Args:
    fun: Function to be differentiated. Its arguments at positions specified by
      ``argnums`` should be arrays, scalars, or standard Python containers.
      Argument arrays in the positions specified by ``argnums`` must be of
      inexact (i.e., floating-point or complex) type. It
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
    A function with the same arguments as ``fun``, that evaluates the gradient
    of ``fun``. If ``argnums`` is an integer then the gradient has the same
    shape and type as the positional argument indicated by that integer. If
    argnums is a tuple of integers, the gradient is a tuple of values with the
    same shapes and types as the corresponding arguments. If ``has_aux`` is True
    then a pair of (gradient, auxiliary_data) is returned.

  For example:

  >>> import jax
  >>>
  >>> grad_tanh = jax.grad(jax.numpy.tanh)
  >>> print(grad_tanh(0.2))
  0.961043
  """
  if reduce_axes:
    raise NotImplementedError("reduce_axes argument to grad is deprecated")
  del reduce_axes
  value_and_grad_f = value_and_grad(fun, argnums, has_aux=has_aux,
                                    holomorphic=holomorphic,
                                    allow_int=allow_int)

  docstr = ("Gradient of {fun} with respect to positional argument(s) "
            "{argnums}. Takes the same arguments as {fun} but returns the "
            "gradient, which has the same shape as the arguments at "
            "positions {argnums}.")

  @wraps(fun, docstr=docstr, argnums=argnums)
  @api_boundary
  def grad_f(*args, **kwargs):
    _, g = value_and_grad_f(*args, **kwargs)
    return g

  @wraps(fun, docstr=docstr, argnums=argnums)
  @api_boundary
  def grad_f_aux(*args, **kwargs):
    (_, aux), g = value_and_grad_f(*args, **kwargs)
    return g, aux

  return grad_f_aux if has_aux else grad_f


def grad(fun: Callable, argnums: int | Sequence[int] = 0,
         has_aux=False, **kwargs) -> Callable:
  """Sparse-aware version of :func:`jax.grad`

  Arguments and return values are the same as :func:`jax.grad`, but when taking
  the gradient with respect to a :class:`jax.experimental.sparse` array, the
  gradient is computed in the subspace defined by the array's sparsity pattern.

  Examples:

    >>> from jax.experimental import sparse
    >>> X = sparse.BCOO.fromdense(jnp.arange(6.))
    >>> y = jnp.ones(6)
    >>> sparse.grad(lambda X, y: X @ y)(X, y)
    BCOO(float32[6], nse=5)
  """
  raw_grad_fun = jax.grad(fun, argnums=argnums, **kwargs)
  argnums = core.concrete_or_error(_ensure_index, argnums)

  @wraps(fun, docstr=raw_grad_fun.__doc__, argnums=argnums)
  @api_boundary
  def grad_fun(*args, **kwargs):
    fun_flat, argnums_flat, args_flat, postprocess_gradients = flatten_fun_for_sparse_ad(fun, argnums, args)
    out = jax.grad(fun_flat, argnums=argnums_flat, has_aux=has_aux, **kwargs)(*args_flat)
    if has_aux:
      return postprocess_gradients(out[0]), out[1]
    return postprocess_gradients(out)
  return grad_fun


def grad(
  fn: Callable[..., Any],
  mdl: Module,
  *primals,
  has_aux: bool = False,
  reduce_axes=(),
  variables: CollectionFilter = True,
  rngs: PRNGSequenceFilter = True,
):
  """A limited, lifted equivalent of ``jax.grad``.

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
        x_grad, y_grad = nn.grad(
            lambda mdl, x, y: mdl(x, y), LearnScale(), x, y)
        return x_grad, y_grad

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
    If ``has_aux`` is ``False``, returns ``grads``, where ``grads`` are the
    gradients for the corresponding primals and do not include the gradients
    for module variables.
    If ``has_aux`` is ``True``, returns a
    ``(grads, aux)`` tuple where ``aux`` is the auxiliary data
    returned by ``fn``.
  """
  if reduce_axes:
    raise NotImplementedError('reduce_axes argument to grad is deprecated')
  del reduce_axes

  value_and_grad_partial = functools.partial(
    value_and_grad,
    fn,
    mdl,
    *primals,
    has_aux=has_aux,
    variables=variables,
    rngs=rngs,
  )

  if has_aux:
    (_, aux), argument_grads = value_and_grad_partial()
    return argument_grads, aux
  else:
    _, argument_grads = value_and_grad_partial()
    return argument_grads


def grad(
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


def grad(
  *,
  argnums: int | DiffState | tp.Sequence[int | DiffState] = 0,
  has_aux: bool = False,
  holomorphic: bool = False,
  allow_int: bool = False,
  reduce_axes: tp.Sequence[AxisName] = (),
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> tp.Callable[[tp.Callable[..., tp.Any]], tp.Callable[..., tp.Any]]: ...


def grad(
  f: tp.Callable[..., tp.Any] | Missing = MISSING,
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
  """Object-aware version of ``jax.grad`` that can handle Modules / graph nodes as
  arguments.

  Example::

    >>> from flax import nnx
    >>> import jax.numpy as jnp
    ...
    >>> m = nnx.Linear(2, 3, rngs=nnx.Rngs(0))
    >>> x = jnp.ones((1, 2))
    >>> y = jnp.ones((1, 3))
    ...
    >>> loss_fn = lambda m, x, y: jnp.mean((m(x) - y) ** 2)
    >>> grad_fn = nnx.grad(loss_fn)
    ...
    >>> grads = grad_fn(m, x, y)
    >>> jax.tree.map(jnp.shape, grads)
    State({
      'bias': Param(
        value=(3,)
      ),
      'kernel': Param(
        value=(2, 3)
      )
    })

  By default, NNX objects are differentiated with respect to all their ``nnx.Param``
  Variables. You can specify which substates are differentiable by passing a ``DiffState``
  object to the ``argnums`` argument. For example, if you want to differentiate only the
  ``kernel`` attribute of the ``Linear`` class, you can use the ``PathContains`` filter::

    >>> m = nnx.Linear(2, 3, rngs=nnx.Rngs(0))
    ...
    >>> kernel_attribute = nnx.PathContains('kernel')
    >>> diff_state = nnx.DiffState(0, kernel_attribute)
    ...
    >>> loss_fn = lambda m, x, y: jnp.mean((m(x) - y) ** 2)
    >>> grad_fn = nnx.grad(loss_fn, argnums=diff_state)
    ...
    >>> grads = grad_fn(m, x, y)
    >>> jax.tree.map(jnp.shape, grads)
    State({
      'kernel': Param(
        value=(2, 3)
      )
    })

  For more information on how to create custom filters, see
  `Using Filters <https://flax.readthedocs.io/en/latest/guides/filters_guide.html>`__
  guide.

  Args:
    fun: Function to be differentiated. Its arguments at positions specified by
      ``argnums`` should be arrays, scalars, graph nodes or standard Python
      containers. Argument arrays in the positions specified by ``argnums`` must
      be of inexact (i.e., floating-point or complex) type. It should return a
      scalar (which includes arrays with shape ``()`` but not arrays with shape
      ``(1,)`` etc.)
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
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references and reference semantics.
      If ``False``, uses tree-mode which treats Modules as regular JAX
      pytrees, avoiding the overhead of the graph protocol. Tree-mode does
      not support ``DiffState`` or shared ``Variable`` references.
    graph_updates: If ``True``, propagates updates on graph structure
      that happen inside the transform to the input graphs, has no
      effect when ``graph=False``. When ``False``, using ``DiffState``
      is not supported.
  """
  if graph is None:
    graph = graphlib.set_graph_mode.current_value()
  if graph_updates is None:
    graph_updates = graphlib.set_graph_updates.current_value()
  if reduce_axes:
    raise NotImplementedError('reduce_axes argument to grad is deprecated')
  del reduce_axes

  if isinstance(f, Missing):
    return functools.partial(
      grad,
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
    _raise_bound_method_error('grad')

  return _grad_general(
    f_unbound,
    argnums,
    has_aux,
    holomorphic,
    allow_int,
    return_value=False,
    graph=graph,
    graph_updates=graph_updates,
  )

