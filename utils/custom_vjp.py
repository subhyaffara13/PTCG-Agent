
def custom_vjp(
  fn: Callable[..., Any],
  forward_fn: Callable[..., Any],
  backward_fn: Callable[..., Any],
  grad_vars: CollectionFilter = 'params',
  nondiff_argnums=(),
):
  """Lifted version of `jax.custom_vjp`.

  `forward_fn` and `backward_fn` together define a custom vjp for `fn`.
  The original `fn` will run in case a vjp (backward gradient) is not computed.

  The `forward_fn` receives the same arguments as `fn` but is expected to return
  a tuple containing the output of `fn(scope, *args)` and the residuals that are
  passed to `backward_fn`.

  The `backward_fn` receives the nondiff arguments, residuals, and the output
  tangents. It should return a tuple containing the variable and input tangents.

  Note that the vjp function returned by `lift.vjp` can be passed as residual
  and used in the `backward_fn`. The scope is unavailable during the backward
  pass. If the scope is required in `backward_fn`, a snapshot of the variables
  can be taken and returned as a residual in the `forward_fn`.

  Example::

    f = nn.dense

    def fwd(scope, x, features):
      y, vjp_fn = lift.vjp(partial(f, features=features), scope, x)
      return y, vjp_fn

    def bwd(features, vjp_fn, y_t):
      params_t, *inputs_t = vjp_fn(y_t)
      params_t = jax.tree_util.tree_map(jnp.sign, params_t)
      return (params_t, *inputs_t)

    dense_sign_grad = lift.custom_vjp(
        f, forward_fn=fwd, backward_fn=bwd, nondiff_argnums=(2,))

  Args:
    fn: The function to define a custom_vjp for. The first argument
      should be a ``Module`` instance.
    forward_fn: A function with the same arguments as `fn` returning an tuple
      with the original output and the residuals that will be passed to
      `backward_fn`.
    backward_fn: arguments are passed as (*nondiff_args, residuals, tangents)
      The function should return a tuple containing the tangents for the
      variable in the collections specified by `grad_vars` and the input
      arguments (except the scope and nondiff args).
    grad_vars: The collections for which a vjp will be computed
      (default: "params").
    nondiff_argnums: arguments for which no vjp is computed.
  Returns:
    A function with the same signature as `fn` with the custom vjp.
  """

  def inner(scope_fn, repack_fn, variable_groups, rng_groups, *args):
    grad_variables, other_variables = variable_groups
    scopes_treedef = None

    def f(grad_variables, *args):
      scope = scope_fn((grad_variables, other_variables), rng_groups)
      y = fn(scope, *args)
      vars_out = repack_fn(scope)
      return y, vars_out

    f = jax.custom_vjp(f, nondiff_argnums=nondiff_argnums)

    def f_fwd(grad_variables, *args):
      nonlocal scopes_treedef
      scopes = scope_fn((grad_variables, other_variables), rng_groups)
      scopes_treedef = jax.tree_util.tree_structure(scopes)
      y, res = forward_fn(scopes, *args)
      vars_out = repack_fn(scopes)
      return (y, vars_out), res

    def f_bwd(*args):
      # the backward function does not pass a lifted scope to the user.
      # Currently, there is no way to have side effects flow out of backward
      # pass. Even without mutation variables would be ill-defined. For example,
      # would we take a snapshot of the variables before or after calling
      # `forward_fn`?
      nondiff_args = args[:-2]
      res, g = args[-2:]  # pylint: disable=unbalanced-tuple-unpacking
      g_y, _ = g
      var_t, *inputs_t = backward_fn(*nondiff_args, res, g_y)
      assert scopes_treedef is not None, 'backward called before forward?!'
      var_t = tuple(scopes_treedef.flatten_up_to(var_t))
      return (var_t, *inputs_t)

    f.defvjp(f_fwd, f_bwd)

    return f(grad_variables, *args)

  variable_in_groups = (grad_vars, True)
  variable_out_groups = (grad_vars, True)
  rng_groups = (True,)
  return pack(
    inner,
    variable_in_groups,
    variable_out_groups,
    rng_groups,
    name='custom_vjp',
  )


def custom_vjp(
  fn: Callable[..., Any],
  forward_fn: Callable[..., Any],
  backward_fn: Callable[..., Any],
  grad_vars: CollectionFilter = 'params',
  nondiff_argnums=(),
):
  """Lifted version of ``jax.custom_vjp``.

  ``forward_fn`` and ``backward_fn`` together define a custom vjp for ``fn``.
  The original ``fn`` will run in case a vjp (backward gradient) is not computed.

  The ``forward_fn`` receives the same arguments as ``fn`` but is expected to return
  a tuple containing the output of ``fn(mdl, *args)`` and the residuals that are
  passed to ``backward_fn``.

  The ``backward_fn`` receives the nondiff arguments, residuals, and the output
  tangents. It should return a tuple containing the variable and input tangents.

  Note that the vjp function returned by ``nn.vjp`` can be passed as residual and
  used in the ``backward_fn``. The scope is unavailable during the backward pass.
  If the module is required in ``backward_fn``, a snapshot of the variables can
  be taken and returned as a residual in the ``forward_fn``.

  Example::

    >>> import flax.linen as nn
    >>> import jax, jax.numpy as jnp

    >>> class Foo(nn.Module):
    ...   @nn.compact
    ...   def __call__(self, x):
    ...     def f(mdl, x):
    ...       return mdl(x)
    ...
    ...     def fwd(mdl, x):
    ...       return nn.vjp(f, mdl, x)
    ...
    ...     def bwd(vjp_fn, y_t):
    ...       params_t, *inputs_t = vjp_fn(y_t)
    ...       params_t = jax.tree_util.tree_map(jnp.sign, params_t)
    ...       return (params_t, *inputs_t)
    ...
    ...     sign_grad = nn.custom_vjp(
    ...         f, forward_fn=fwd, backward_fn=bwd)
    ...     return sign_grad(nn.Dense(1), x).reshape(())

    >>> x = jnp.ones((2,))
    >>> variables = Foo().init(jax.random.key(0), x)
    >>> grad = jax.grad(Foo().apply)(variables, x)

  Args:
    fn: The function to define a custom_vjp for.
    forward_fn: A function with the same arguments as ``fn`` returning an tuple
      with the original output and the residuals that will be passed to
      ``backward_fn``.
    backward_fn: arguments are passed as
      ``(*nondiff_args, residuals, tangents)`` The function should return a
      tuple containing the tangents for the variable in the collections
      specified by ``grad_vars`` and the input arguments (except the module and
      nondiff args).
    grad_vars: The collections for which a vjp will be computed
      (default: "params").
    nondiff_argnums: arguments for which no vjp is computed.
  Returns:
    A function with the same signature as ``fn`` with the custom vjp.
  """

  def shared_forward_fn(*args, needs_residual, **kwargs):
    if needs_residual:
      return forward_fn(*args, **kwargs)
    else:
      return fn(*args, **kwargs)

  return decorator_lift_transform(
    _custom_vjp_single_scope_fn,
    shared_forward_fn,
    backward_fn=backward_fn,
    grad_vars=grad_vars,
    nondiff_argnums=nondiff_argnums,
    multi_scope=False,
  )


def custom_vjp(
  fun: tp.Callable[..., A],
  *,
  nondiff_argnums: tuple[int | DiffState, ...] = (),
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> CustomVjp[A] | SimpleCustomVjp[A]: ...


def custom_vjp(
  *,
  nondiff_argnums: tuple[int | DiffState, ...] = (),
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> tp.Callable[[tp.Callable[..., A]], CustomVjp[A] | SimpleCustomVjp[A]]: ...


def custom_vjp(
  fun: tp.Callable[..., A] | Missing = MISSING,
  *,
  nondiff_argnums: tuple[int | DiffState, ...] = (),
  graph: bool | None = None,
  graph_updates: bool | None = None,
) -> CustomVjp[A] | SimpleCustomVjp[A] | tp.Callable[[tp.Callable[..., A]], CustomVjp[A] | SimpleCustomVjp[A]]:
  """Reference aware version of
  `jax.custom_vjp <https://jax.readthedocs.io/en/latest/_autosummary/jax.custom_vjp.html>`__.

  ``nnx.custom_vjp`` accepts Modules and other Flax NNX objects as arguments. The main difference
  with the JAX version is that, because Modules follow reference semantics, they propagate the State
  updates for the inputs as auxiliary outputs. This means that the incoming gradients in the ``bwd`` function
  will have the form ``(input_updates_g, out_g)`` where ``input_updates_g`` is the gradient updated state of
  the inputs w.r.t. to the inputs. All Module terms on the inputs will an associated ``State`` term in
  ``input_updates_g``, while all non-Module terms will appear as None. The shape of the tangent will be
  expected to have the same shape as the input, with ``State`` terms in place of the corresponding Module terms.

  Example::

    >>> import jax
    >>> import jax.numpy as jnp
    >>> from flax import nnx
    ...
    >>> class Foo(nnx.Module):
    ...   def __init__(self, x, y):
    ...     self.x = nnx.Param(x)
    ...     self.y = nnx.Param(y)
    ...
    >>> @nnx.custom_vjp
    ... def f(m: Foo):
    ...   return jnp.sin(m.x) * m.y
    ...
    >>> def f_fwd(m: Foo):
    ...   return f(m), (jnp.cos(m.x), jnp.sin(m.x), m)
    ...
    >>> def f_bwd(res, g):
    ...   input_updates_g, out_g = g
    ...   cos_x, sin_x, m = res
    ...   (m_updates_g,) = input_updates_g
    ...   m_g = jax.tree.map(lambda x: x, m_updates_g) # create copy
    ...
    ...   m_g['x'][...] = cos_x * out_g * m.y
    ...   m_g['y'][...] = sin_x * out_g
    ...   return (m_g,)
    ...
    >>> f.defvjp(f_fwd, f_bwd)
    ...
    >>> m = Foo(x=jnp.array(1.), y=jnp.array(2.))
    >>> grads = nnx.grad(f)(m)
    ...
    >>> jax.tree.map(jnp.shape, grads)
    State({
      'x': Param(
        value=()
      ),
      'y': Param(
        value=()
      )
    })

  Note that the State objects that represent Module terms on ``input_updates_g`` have the
  same shape as the State objects expected in the output tanget. This means that you can
  usually just copy them from ``input_updates_g`` and update them with their corresponding
  gradient values.

  You can select which substates are differentiable (have a tangent) for Modules and other
  graph nodes by passing a ``DiffState`` to ``nondiff_argnums``. For example, if you want to
  differentiate only the ``x`` attribute of the ``Foo`` class, you can do the following::

    >>> x_attribute = nnx.PathContains('x')
    >>> diff_state = nnx.DiffState(0, x_attribute)
    ...
    >>> @nnx.custom_vjp(nondiff_argnums=(diff_state,))
    ... def f(m: Foo):
    ...   return jnp.sin(m.x) * m.y  # type: ignore

    >>> def f_fwd(m: Foo):
    ...   y = f(m)
    ...   res = (jnp.cos(m.x), m)  # type: ignore
    ...   return y, res
    ...
    >>> def f_bwd(res, g):
    ...   input_updates_g, out_g = g
    ...   cos_x, m = res
    ...   (m_updates_g,) = input_updates_g
    ...   m_g = jax.tree.map(lambda x: x, m_updates_g) # create copy
    ...
    ...   m_g.x[...] = cos_x * out_g * m.y
    ...   del m_g['y'] # y is not differentiable
    ...   return (m_g,)

    >>> f.defvjp(f_fwd, f_bwd)
    ...
    >>> m = Foo(x=jnp.array(1.), y=jnp.array(2.))
    >>> grad = nnx.grad(f, argnums=nnx.DiffState(0, x_attribute))(m)
    ...
    >>> jax.tree.map(jnp.shape, grad)
    State({
      'x': Param(
        value=()
      )
    })

  Note that ``grad`` cannot calculate gradients for states that don't have a tangent
  defined by ``custom_vjp``, in the example above we reuse the same ``x_attribute``
  filter to keep ``custom_vjp`` and ``grad`` in sync.

  **graph_updates=False**

  When ``graph_updates=False`` or ``graph=False``, the behavior is closer to
  ``jax.custom_vjp``: the ``bwd`` function receives ``out_g`` directly, and
  tangent types are the same as the input types, this means the tangent for a
  Module is a Module instance with gradient values set on its attributes.
  This mode does not support ``DiffState`` in ``nondiff_argnums``. Additionally,
  Variables in differentiable arguments cannot be mutated inside ``f``. If
  mutations are needed, pass the relevant Variables through a non-differentiable
  argument instead.

  Example::

    >>> @nnx.custom_vjp(graph_updates=False)
    ... def f(m: Foo):
    ...   return jnp.sin(m.x) * m.y
    ...
    >>> def f_fwd(m: Foo):
    ...   return f(m), (jnp.cos(m.x), jnp.sin(m.x), m)
    ...
    >>> def f_bwd(res, g):
    ...   cos_x, sin_x, m = res
    ...   m_g = nnx.clone(m)
    ...   m_g.x[...] = cos_x * g * m.y
    ...   m_g.y[...] = sin_x * g
    ...   return (m_g,)
    ...
    >>> f.defvjp(f_fwd, f_bwd)

  Args:
    fun: Callable base function.
    nondiff_argnums: Tuple of integers or DiffState objects specifying the
      argument indices that are not differentiated. By default all arguments are
      differentiated. Integers cannot be used to mark graph nodes such as Modules
      as non-differentiable, in this case use a DiffState object. DiffState objects
      define the set of differentiable substates, contrary to what the name of this
      argument suggests, this is done for compatibility with ``grad``.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references and reference semantics.
      If ``False``, uses tree-mode which treats Modules as regular JAX
      pytrees, avoiding the overhead of the graph protocol. Tree-mode does
      not support ``DiffState`` in ``nondiff_argnums``.
    graph_updates: If ``True``, propagates updates on graph structure
      that happen inside the transform to the input graphs, has no
      effect when ``graph=False``. When ``False``, using ``DiffState``
      is not supported.

  """
  if graph is None:
    graph = graphlib.set_graph_mode.current_value()
  if graph_updates is None:
    graph_updates = graphlib.set_graph_updates.current_value()
  if isinstance(fun, Missing):
    return functools.partial(
      custom_vjp, nondiff_argnums=nondiff_argnums, graph=graph,
      graph_updates=graph_updates,
    )

  # Detect bound nnx.Module methods and raise error.
  fun_unbound, _, was_bound = _resolve_bound_callable(fun)
  if was_bound:
    _raise_bound_method_error('custom_vjp')

  extract.check_prefix(
    nondiff_argnums, 'nondiff_argnums', 'custom_vjp', graph, graph_updates
  )

  if not graph or not graph_updates:
    return SimpleCustomVjp(fun_unbound, nondiff_argnums, graph=graph)  # type: ignore[arg-type]

  return CustomVjp(fun_unbound, nondiff_argnums)

