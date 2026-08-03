import functools
from typing import Any, Callable, Tuple

def checkpoint(
    function,
    *args,
    use_reentrant: bool | None = None,
    context_fn: Callable[[], Tuple[ContextManager, ContextManager]] = noop_context_fn,
    determinism_check: str = _DEFAULT_DETERMINISM_MODE,
    debug: bool = False,
    early_stop: bool = True,
    **kwargs
):
    r"""Checkpoint a model or part of the model.

    Activation checkpointing is a technique that trades compute for memory.
    By default, tensors computed during the forward pass are kept alive until
    they are used in gradient computations in the backward pass. To reduce this
    memory usage, tensors produced in the passed :attr:`function` are not kept
    alive until the backward pass. Instead, any passed tensors in :attr:`args`
    are kept alive, and the unsaved tensors are recomputed by re-invoking
    :attr:`function` in the backward pass as needed for gradient computation.
    Activation checkpointing can be applied to any part of a model -- this is
    sometimes described as "checkpointing" that part of the model.

    There are currently two checkpointing implementations available, determined
    by the :attr:`use_reentrant` parameter. It is recommended that you use
    ``use_reentrant=False``. Please refer the note below for a discussion of
    their differences.

    .. warning::

        If the :attr:`function` invocation during the backward pass differs
        from the forward pass, e.g., due to a global variable, the checkpointed
        version may not be equivalent, potentially causing an
        error being raised or leading to silently incorrect gradients.

    .. warning::

        The ``use_reentrant`` parameter should be passed explicitly. In version
        2.9 we will raise an exception if ``use_reentrant`` is not passed.
        If you are using the ``use_reentrant=True`` variant, please refer to the
        note below for important considerations and potential limitations.

    .. note::

        The reentrant variant of checkpoint (``use_reentrant=True``) and
        the non-reentrant variant of checkpoint (``use_reentrant=False``)
        differ in the following ways:

        * Non-reentrant checkpoint stops recomputation as soon as all needed
          intermediate activations have been recomputed. This feature is enabled
          by default, but can be disabled with :func:`set_checkpoint_early_stop`.
          Reentrant checkpoint always recomputes :attr:`function` in its
          entirety during the backward pass.

        * The reentrant variant does not record the autograd graph during the
          forward pass, as it runs with the forward pass under
          :func:`torch.no_grad`. The non-reentrant version does record the
          autograd graph, allowing one to perform backward on the graph within
          checkpointed regions.

        * The reentrant checkpoint only supports the
          :func:`torch.autograd.backward` API for the backward pass without its
          `inputs` argument, while the non-reentrant version supports all ways
          of performing the backward pass.

        * At least one input and output must have ``requires_grad=True`` for the
          reentrant variant. If this condition is unmet, the checkpointed part
          of the model will not have gradients. The non-reentrant version does
          not have this requirement.

        * The reentrant version does not consider tensors in nested structures
          (e.g., custom objects, lists, dicts, etc) as participating in
          autograd, while the non-reentrant version does.

        * The reentrant checkpoint does not support checkpointed regions with
          detached tensors from the computational graph, whereas the
          non-reentrant version does. For the reentrant variant, if the
          checkpointed segment contains tensors detached using ``detach()`` or
          with :func:`torch.no_grad`, the backward pass will raise an error.
          This is because ``checkpoint`` makes all the outputs require gradients
          and this causes issues when a tensor is defined to have no gradient in
          the model. To avoid this, detach the tensors outside of the
          ``checkpoint`` function.

    Args:
        function: describes what to run in the forward pass of the model or
            part of the model. It should also know how to handle the inputs
            passed as the tuple. For example, in LSTM, if user passes
            ``(activation, hidden)``, :attr:`function` should correctly use the
            first input as ``activation`` and the second input as ``hidden``
        args: tuple containing inputs to the :attr:`function`

    Keyword args:
        preserve_rng_state(bool, optional):  Omit stashing and restoring
            the RNG state during each checkpoint. Note that under torch.compile,
            this flag doesn't take effect and we always preserve RNG state.
            Default: ``True``
        use_reentrant(bool):
            specify whether to use the activation checkpoint variant that
            requires reentrant autograd. This parameter should be passed
            explicitly. In version 2.9 we will raise an exception if
            ``use_reentrant`` is not passed. If ``use_reentrant=False``,
            ``checkpoint`` will use an implementation that does not require
            reentrant autograd. This allows ``checkpoint`` to support additional
            functionality, such as working as expected with
            ``torch.autograd.grad`` and support for keyword arguments input into
            the checkpointed function.
        context_fn(Callable, optional): A callable returning a tuple of two
            context managers. The function and its recomputation will be run
            under the first and second context managers respectively.
            This argument is only supported if ``use_reentrant=False``.
        determinism_check(str, optional): A string specifying the determinism
            check to perform. By default it is set to ``"default"`` which
            compares the shapes, dtypes, and devices of the recomputed tensors
            against those the saved tensors. To turn off this check, specify
            ``"none"``. Currently these are the only two supported values.
            Please open an issue if you would like to see more determinism
            checks. This argument is only supported if ``use_reentrant=False``,
            if ``use_reentrant=True``, the determinism check is always disabled.
        debug(bool, optional): If ``True``, error messages will also include
            a trace of the operators ran during the original forward computation
            as well as the recomputation. This argument is only supported if
            ``use_reentrant=False``.
        early_stop(bool, optional): If ``True``, non-reentrant checkpoint stops
            recomputation as soon as it has computed all needed Tensors. This
            argument is ignored if ``use_reentrant=True``. Can be overridden
            globally using :func:`set_checkpoint_early_stop` context manager.
            Default: ``True``.

    Returns:
        Output of running :attr:`function` on :attr:`*args`
    """
    if use_reentrant is None:
        warnings.warn(
            "torch.utils.checkpoint: the use_reentrant parameter should be "
            "passed explicitly. Starting in PyTorch 2.9, calling checkpoint "
            "without use_reentrant will raise an exception. use_reentrant=False is "
            "recommended, but if you need to preserve the current default "
            "behavior, you can pass use_reentrant=True. Refer to docs for more "
            "details on the differences between the two variants.",
            stacklevel=2
        )
        use_reentrant = True

    # Hack to mix *args with **kwargs in a python 2.7-compliant way
    preserve = kwargs.pop("preserve_rng_state", True)
    if kwargs and use_reentrant:
        raise ValueError(
            "Unexpected keyword arguments: " + ",".join(arg for arg in kwargs)
        )

    if use_reentrant:
        if context_fn is not noop_context_fn or debug is not False:
            raise ValueError(
                "Passing `context_fn` or `debug` is only supported when "
                "use_reentrant=False."
            )
        return CheckpointFunction.apply(function, preserve, *args)
    else:
        gen = _checkpoint_without_reentrant_generator(
            function, preserve, context_fn, determinism_check, debug, early_stop, *args, **kwargs
        )
        # Runs pre-forward logic
        next(gen)
        ret = function(*args, **kwargs)
        # Runs post-forward logic
        try:
            next(gen)
        except StopIteration:
            return ret


def checkpoint(module: nn.Module, **kwargs) -> nn.Module:
    r"""
    This is a composable activation checkpointing API. Unlike functional
    activation checkpointing APIs, this one does not require changing model
    source code. Unlike ``nn.Module`` wrapper activation checkpointing APIs,
    this one does not modify model structure or fully-qualified names either.
    Under the hood, it registers activation checkpointing logic as pre- and
    post-forward hooks. Hence, this API can be easily applied to any model or
    sub-modules in the model.

    Args:
        module (nn.Module): the target model or sub-module to apply activation
            checkpointing.

    Example::
        >>> # xdoctest: +SKIP
        >>> import torch.nn as nn
        >>>
        >>> class MyModel(nn.Module):
        >>>     def __init__(self) -> None:
        >>>         super().__init__()
        >>>         self.l1 = nn.Linear(10, 10)
        >>>         self.l2 = nn.Linear(10, 10)
        >>>
        >>>     def forward(self, x):
        >>>         return self.l2(self.l1(x))
        >>>
        >>> model = MyModel()
        >>> checkpoint(model.l1)  # apply activation checkpointing only to l1
        >>> model(torch.zeros(2, 10)).sum().backward()

    """
    torch._C._log_api_usage_once("torch.distributed.checkpoint")

    use_reentrant = kwargs.pop("use_reentrant", False)
    if use_reentrant:
        raise NotImplementedError(
            "use_reentrant=True is not supported in composable checkpoint. "
            "Please use torch.utils.checkpoint.checkpoint instead."
        )
    preserve_rng_state = kwargs.pop("preserve_rng_state", True)
    user_context_fns = kwargs.pop("context_fn", None)
    determinism_check = kwargs.pop("determinism_check", _DEFAULT_DETERMINISM_MODE)
    debug = kwargs.pop("debug", False)
    early_stop = kwargs.pop("early_stop", True)

    if kwargs:
        raise ValueError(
            "Unexpected keyword arguments: " + ",".join(arg for arg in kwargs)
        )

    def forward_pre_hook(
        module: nn.Module, args: tuple[Any, ...], kwargs: dict[str, Any]
    ) -> None:
        if checkpoint.state(module).enable_hook:

            def context_fns():
                if user_context_fns is not None:
                    ctx1, ctx2 = user_context_fns()
                    return ctx1, _no_hook(module, ctx2)
                else:
                    return nullcontext(), _no_hook(module)

            gen = _checkpoint_without_reentrant_generator(
                module,
                preserve_rng_state,
                context_fns,
                determinism_check,
                debug,
                early_stop,
                *args,
                **kwargs,
            )
            checkpoint.state(module)._ac_generator = gen
            next(gen)

    def forward_hook(module: nn.Module, inputs: tuple[Any, ...], output: Any) -> Any:
        if checkpoint.state(module).enable_hook:
            try:
                gen = checkpoint.state(module)._ac_generator
                if gen is None:
                    raise AssertionError
                next(gen)
            except StopIteration:
                pass
            else:
                raise RuntimeError(
                    "Expected non-reentrant activation checkpoint generator to be exhausted, but it was not!"
                )

        #  Ensure that we no longer hold on to the generator. always_call=True helps ensure we
        # clear this even in the case of exception in fwd pass.
        checkpoint.state(module)._ac_generator = None

    checkpoint.state(module).enable_hook = True
    module.register_forward_pre_hook(forward_pre_hook, with_kwargs=True)
    module.register_forward_hook(forward_hook, prepend=True, always_call=True)
    return module


def checkpoint(fun: Callable, *, prevent_cse: bool | Sequence[bool] = True,
               policy: Callable[..., bool] | None = None,
               static_argnums: int | tuple[int, ...] = (),
               static_argnames: str | Iterable[str] = (),
               concrete: bool | DeprecatedArg = DeprecatedArg()) -> Callable:
  """Make ``fun`` recompute internal linearization points when differentiated.

  The :func:`jax.checkpoint` decorator, aliased to :func:`jax.remat`, provides a
  way to trade off computation time and memory cost in the context of automatic
  differentiation, especially with reverse-mode autodiff like :func:`jax.grad`
  and :func:`jax.vjp` but also with :func:`jax.linearize`.

  When differentiating a function in reverse-mode, by default all the
  linearization points (e.g. inputs to elementwise nonlinear primitive
  operations) are stored when evaluating the forward pass so that they can be
  reused on the backward pass. This evaluation strategy can lead to a high
  memory cost, or even to poor performance on hardware accelerators where memory
  access is much more expensive than FLOPs.

  An alternative evaluation strategy is for some of the linearization points to
  be recomputed (i.e. rematerialized) rather than stored. This approach can
  reduce memory usage at the cost of increased computation.

  This function decorator produces a new version of ``fun`` which follows
  the rematerialization strategy rather than the default store-everything
  strategy. That is, it returns a new version of ``fun`` which, when
  differentiated, doesn't store any of its intermediate linearization points.
  Instead, these linearization points are recomputed from the function's saved
  inputs.

  See the examples below.

  Args:
    fun: Function for which the autodiff evaluation strategy is to be changed
      from the default of storing all intermediate linearization points to
      recomputing them. Its arguments and return value should be arrays,
      scalars, or (nested) standard Python containers (tuple/list/dict) thereof.
    prevent_cse: Optional, boolean keyword-only argument indicating whether to
      prevent common subexpression elimination (CSE) optimizations in the HLO
      generated from differentiation. This CSE prevention has costs because it
      can foil other optimizations, and because it can incur high overheads on
      some backends, especially GPU. The default is True because otherwise,
      under a :func:`~jax.jit` or :func:`~jax.pmap`, CSE can defeat the purpose
      of this decorator.
      But in some settings, like when used inside a :func:`~jax.lax.scan`, this
      CSE prevention mechanism is unnecessary, in which case ``prevent_cse`` can
      be set to False.
    static_argnums: Optional, int or sequence of ints, a keyword-only argument
      indicating which argument values on which to specialize for tracing and
      caching purposes. Specifying arguments as static can avoid
      ConcretizationTypeErrors when tracing, but at the cost of more retracing
      overheads. See the example below.
    policy: Optional, callable keyword-only argument. It should be one of the
      attributes of ``jax.checkpoint_policies``. The callable takes as input a
      type-level specification of a first-order primitive application and
      returns a boolean indicating whether the corresponding output value(s) can
      be saved as residuals (or instead must be recomputed in the (co)tangent
      computation if needed).
    concrete: Optional boolean; deprecated. Will raise a DeprecationWarning if
      used, and passing True will result in a NotImplementedError.

  Returns:
    A function (callable) with the same input/output behavior as ``fun`` but
    which, when differentiated using e.g. :func:`jax.grad`, :func:`jax.vjp`, or
    :func:`jax.linearize`, recomputes rather than stores intermediate
    linearization points, thus potentially saving memory at the cost of extra
    computation.

  Here is a simple example:

  >>> import jax
  >>> import jax.numpy as jnp

  >>> @jax.checkpoint
  ... def g(x):
  ...   y = jnp.sin(x)
  ...   z = jnp.sin(y)
  ...   return z
  ...
  >>> jax.value_and_grad(g)(2.0)
  (Array(0.78907233, dtype=float32, weak_type=True), Array(-0.2556391, dtype=float32, weak_type=True))

  Here, the same value is produced whether or not the :func:`jax.checkpoint`
  decorator is present. When the decorator is not present, the values
  ``jnp.cos(2.0)`` and ``jnp.cos(jnp.sin(2.0))`` are computed on the forward
  pass and are stored for use in the backward pass, because they are needed
  on the backward pass and depend only on the primal inputs. When using
  :func:`jax.checkpoint`, the forward pass will compute only the primal outputs
  and only the primal inputs (``2.0``) will be stored for the backward pass.
  At that time, the value ``jnp.sin(2.0)`` is recomputed, along with the values
  ``jnp.cos(2.0)`` and ``jnp.cos(jnp.sin(2.0))``.

  While :func:`jax.checkpoint` controls what values are stored from the
  forward-pass to be used on the backward pass, the total amount of memory
  required to evaluate a function or its VJP depends on many additional internal
  details of that function. Those details include which numerical primitives are
  used, how they're composed, where jit and control flow primitives like scan
  are used, and other factors.

  The :func:`jax.checkpoint` decorator can be applied recursively to express
  sophisticated autodiff rematerialization strategies. For example:

  >>> def recursive_checkpoint(funs):
  ...   if len(funs) == 1:
  ...     return funs[0]
  ...   elif len(funs) == 2:
  ...     f1, f2 = funs
  ...     return lambda x: f1(f2(x))
  ...   else:
  ...     f1 = recursive_checkpoint(funs[:len(funs)//2])
  ...     f2 = recursive_checkpoint(funs[len(funs)//2:])
  ...     return lambda x: f1(jax.checkpoint(f2)(x))
  ...

  If ``fun`` involves Python control flow that depends on argument values,
  it may be necessary to use the ``static_argnums`` parameter. For example,
  consider a boolean flag argument::

    from functools import partial

    @partial(jax.checkpoint, static_argnums=(1,))
    def foo(x, is_training):
      if is_training:
        ...
      else:
        ...

  Here, the use of ``static_argnums`` allows the ``if`` statement's condition
  to depends on the value of ``is_training``. The cost to using
  ``static_argnums`` is that it introduces re-tracing overheads across calls:
  in the example, ``foo`` is re-traced every time it is called with a new value
  of ``is_training``. In some situations, ``jax.ensure_compile_time_eval``
  is needed as well::

    @partial(jax.checkpoint, static_argnums=(1,))
    def foo(x, y):
      with jax.ensure_compile_time_eval():
        y_pos = y > 0
      if y_pos:
        ...
      else:
        ...

  As an alternative to using ``static_argnums`` (and
  ``jax.ensure_compile_time_eval``), it may be easier to compute some values
  outside the :func:`jax.checkpoint`-decorated function and then close over them.
  """
  # TODO(jakevdp): Remove the concrete argument in JAX v0.11.0.
  if not isinstance(concrete, DeprecatedArg):
    concrete_msg = (
        "The `concrete` option to `jax.checkpoint` was deprecated in JAX"
        " v0.8.2, and removed in JAX v0.10.0."
        " In its place please use `static_argnums`; for details refer to"
        " https://docs.jax.dev/en/latest/jep/11830-new-remat-checkpoint.html."
    )
    raise NotImplementedError(concrete_msg)
  del concrete

  if isinstance(static_argnums, int):
    static_argnums = static_argnums,
  if isinstance(prevent_cse, Sequence):
    prevent_cse = tuple(prevent_cse)
  if not isinstance(prevent_cse, (tuple, bool)):
    raise TypeError("prevent_cse must be a bool or tuple of bools, got "
                    f"{type(prevent_cse)=}")

  if config.remat3.value:
    policy = None if policy is nothing_saveable else policy
    return remat3(fun, policy=policy, static_argnums=static_argnums,
                  static_argnames=static_argnames)

  @wraps(fun)
  @api_boundary
  def fun_remat(*args, **kwargs):
    debug = api_util.debug_info(
        "checkpoint / remat", fun,
        args, kwargs, static_argnums=static_argnums)
    fun_, args = _remat_static_argnums(fun, static_argnums, args)
    args_flat, in_tree = tracing_registry.flatten((args, kwargs))
    api_util.check_no_transformed_refs_args(lambda: debug, args_flat)
    in_avals = [core.shaped_abstractify(x) for x in args_flat]
    jaxpr, consts, out_tree = _trace_to_jaxpr(fun_, in_tree, tuple(in_avals), debug)
    if isinstance(prevent_cse, tuple):
      cse_args = (tuple(args), kwargs) if kwargs else tuple(args)
      cse = (False,) * len(consts) + tuple(broadcast_prefix(prevent_cse, cse_args))
    else:
      cse = prevent_cse
    out_flat = remat_p.bind(
        *consts, *args_flat, jaxpr=jaxpr, prevent_cse=cse, differentiated=False,
        policy=policy)
    return tree_unflatten(out_tree, out_flat)
  return fun_remat


def checkpoint(
  fn: Callable[..., Any],
  variables: CollectionFilter = True,
  rngs: PRNGSequenceFilter = True,
  concrete: bool = False,
  prevent_cse: bool = True,
  static_argnums: int | tuple[int, ...] = (),
  policy: Callable[..., bool] | None = None,
) -> Callable[..., Any]:
  """Lifted version of ``jax.checkpoint``.

  This function is aliased to ``lift.remat`` just like ``jax.remat``.

  Args:
    fn: scope function for which intermediate computations should be re-computed
      when computing gradients.
    variables: The variable collections that are lifted. By default all
      collections are lifted.
    rngs: The PRNG sequences that are lifted. By default all PRNG sequences are
      lifted.
    concrete: Optional, boolean indicating whether ``fun`` may involve
      value-dependent Python control flow (default ``False``). Support for such
      control flow is optional, and disabled by default, because in some
      edge-case compositions with :func:`jax.jit` it can lead to some extra
      computation.
    prevent_cse: Optional, boolean indicating whether to prevent common
      subexpression elimination (CSE) optimizations in the HLO generated from
      differentiation. This CSE prevention has costs because it can foil other
      optimizations, and because it can incur high overheads on some backends,
      especially GPU. The default is True because otherwise, under a ``jit`` or
      ``pmap``, CSE can defeat the purpose of this decorator. But in some
      settings, like when used inside a ``scan``, this CSE prevention mechanism
      is unnecessary, in which case ``prevent_cse`` can be set to False.
    static_argnums: Optional, int or sequence of ints, indicates which argument
      values on which to specialize for tracing and caching purposes. Specifying
      arguments as static can avoid ConcretizationTypeErrors when tracing, but
      at the cost of more retracing overheads.
    policy: Experimental checkpoint policy, see ``jax.checkpoint``.

  Returns:
    A wrapped version of ``fn``. When computing gradients intermediate
    computations will be re-computed when computing gradients.
  """

  def inner(scope_fn, repack_fn, variable_groups, rng_groups, *args, **kwargs):
    # add 2 to each static_argnums because we add two initial arguments to rematted
    static_argnums_ = jax.tree_util.tree_map(lambda x: x + 2, static_argnums)

    # After JAX v0.3.16, concrete=False is a no-op and concrete=True raises
    # NotImplementedError. Starting in JAX v0.8.2, the concrete argument is
    # deprecated and will be removed in the future.
    if concrete:
      raise NotImplementedError(
          "The concrete argument is deprecated. Use static_argnums instead."
          " for more information, see"
          " https://docs.jax.dev/en/latest/jep/11830-new-remat-checkpoint.html"
      )

    @functools.partial(
      jax.remat,
      static_argnums=static_argnums_,
      prevent_cse=prevent_cse,
      policy=policy,
    )
    @functools.wraps(fn)
    def rematted(variable_groups, rng_groups, *args, **kwargs):
      scope = scope_fn(variable_groups, rng_groups)
      y = fn(scope, *args, **kwargs)
      return y, repack_fn(scope)

    return rematted(variable_groups, rng_groups, *args, **kwargs)

  return pack(
    inner,
    (variables,),
    (variables,),
    (rngs,),
    name='remat',
    enable_kwargs=True,
  )


def checkpoint(
  target: Target,
  variables: CollectionFilter = True,
  rngs: PRNGSequenceFilter = True,
  concrete: bool = False,
  prevent_cse: bool = True,
  static_argnums: int | tuple[int, ...] = (),
  policy: Callable[..., bool] | None = None,
  methods=None,
) -> Target:
  """Lifted version of ``jax.checkpoint``.

  Checkpointing is a technique for reducing memory usage by recomputing
  activations during backpropagation. When training large models, it can be
  helpful to checkpoint parts of the model to trade off memory usage for
  additional computation.

  Example::

    >>> import jax
    >>> import jax.numpy as jnp
    >>> import flax.linen as nn
    ...
    >>> class CheckpointedMLP(nn.Module):
    ...   @nn.checkpoint
    ...   @nn.compact
    ...   def __call__(self, x):
    ...     x = nn.Dense(128)(x)
    ...     x = nn.relu(x)
    ...     x = nn.Dense(1)(x)
    ...     return x
    ...
    >>> model = CheckpointedMLP()
    >>> variables = model.init(jax.random.key(0), jnp.ones((1, 16)))

  This function is aliased to ``remat`` just like ``jax.remat``.

  Args:
    target: a ``Module`` or a function taking a ``Module``
      as its first argument. intermediate computations will be
      re-computed when computing gradients for the target.
    variables: The variable collections that are lifted. By default all
      collections are lifted.
    rngs: The PRNG sequences that are lifted. By default all PRNG sequences
      are lifted.
    concrete: Optional, boolean indicating whether ``fun`` may involve
      value-dependent Python control flow (default ``False``). Support for such
      control flow is optional, and disabled by default, because in some
      edge-case compositions with :func:`jax.jit` it can lead to some extra
      computation.
    prevent_cse: Optional, boolean indicating whether to prevent common
      subexpression elimination (CSE) optimizations in the HLO generated from
      differentiation. This CSE prevention has costs because it can foil other
      optimizations, and because it can incur high overheads on some backends,
      especially GPU. The default is True because otherwise, under a ``jit`` or
      ``pmap``, CSE can defeat the purpose of this decorator. But in some
      settings, like when used inside a ``scan``, this CSE prevention mechanism
      is unnecessary, in which case ``prevent_cse`` should be set to False.
    static_argnums: Optional, int or sequence of ints, indicates which argument
      values on which to specialize for tracing and caching purposes. Specifying
      arguments as static can avoid ConcretizationTypeErrors when tracing, but
      at the cost of more retracing overheads.
    policy: Experimental checkpoint policy, see ``jax.checkpoint``.
    methods: An optional list of method names that will be lifted, if ``methods``
      is None (default) only the ``__call__`` method will be lifted. If``target``
      is a function, ``methods`` is ignored.

  Returns:
    A wrapped version of ``target``. When computing gradients intermediate
    computations will be re-computed on the backward pass.
  """
  # subtract 1 from each static_argnums because 'self' is not passed to the
  # lifted function
  static_argnums = jax.tree_util.tree_map(lambda x: x - 1, static_argnums)
  return lift_transform(
      lift.checkpoint,
      target,
      variables=variables,
      rngs=rngs,
      concrete=concrete,
      static_argnums=static_argnums,
      prevent_cse=prevent_cse,
      policy=policy,
      methods=methods,
  )

