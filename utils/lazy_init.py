
def lazy_init(input_device: torch.device | None = None):
    if torch._C._has_mkldnn and config.cpp.weight_prepack:
        from .mkldnn_fusion import _mkldnn_weight_pack_init

        _mkldnn_weight_pack_init()

    from .binary_folding import binary_folding_init

    addmm_patterns_init()
    binary_folding_init()


def lazy_init(input_device: torch.device | None = None):
    from .fuse_attention import _sfdp_init
    from .misc_patterns import _misc_patterns_init
    from .pad_mm import _pad_mm_init

    _pad_mm_init(input_device)
    _sfdp_init(input_device)
    _misc_patterns_init(input_device)


def lazy_init(input_device: torch.device | None = None):
    if torch._C._has_mkldnn:
        from . import decompose_mem_bound_mm  # noqa: F401
        from .mkldnn_fusion import _mkldnn_fusion_init

        _mkldnn_fusion_init()
    else:
        from .quantization import _register_woq_lowerings

        _register_woq_lowerings()

    # Put this patterns in post-grad pass rather than joint-graph
    # pass since otherwise there will be perf/peak-memory regression:
    # https://github.com/pytorch/pytorch/issues/148141
    register_replacement(
        # pyrefly: ignore [bad-argument-type]
        prepare_softmax_pattern,
        # pyrefly: ignore [bad-argument-type]
        prepare_softmax_replacement,
        [torch.empty(4, 8)],
        scalar_workaround=dict(dim=-1),
        # pyrefly: ignore [bad-argument-type]
        trace_fn=fwd_only,
        # pyrefly: ignore [bad-argument-type]
        pass_dicts=pass_patterns[1],
        extra_check=prepare_softmax_extra_check,
    )


def lazy_init(input_device: torch.device | None = None):
    from . import (  # noqa: F401  # noqa: F401
        apply_gumbel_max_trick,
        efficient_conv_bn_eval,
        split_cat,
    )

    if config.is_fbcode():
        from . import fb  # type: ignore[attr-defined]  # noqa: F401


def lazy_init(fn):
  """Lazily evaluates a function by using the shapes of the inputs.

  The returned function accepts a combination of JAX values and
  ``jax.ShapeDtypeStruct`` instances for the inputs for which we
  don't need concrete values (only the shape and dtype).

  This API is used by ``core.lazy_init`` or ``Module.lazy_init``
  to initialize variables without doing any actual computation on the
  inputs.

  Args:
    fn: the function to be lazily evaluated.
  Returns:
    A new function that accepts a mix of concrete values and
    ``jax.ShapeDtypeStruct`` instances.
  """

  @functools.wraps(fn)
  def wrapper(*args, **kwargs):
    # TODO(mattjj,jheek): use a public JAX API
    # flatten fn and prepare for internal JAX transform
    inputs_flat, in_tree = jax.tree_util.tree_flatten((args, kwargs))
    debug_info = jax.api_util.debug_info("lazy_init", fn, (in_tree,), {})
    f_flat, out_tree = jax.api_util.flatten_fun(
      lu.wrap_init(fn, debug_info=debug_info), in_tree)
    # map inputs to PartialVal known/unknown
    # only the computations depending on knowns will be executed
    in_pvals = [_maybe_unknown(x) for x in inputs_flat]
    _, out_pvals, _ = pe.trace_to_jaxpr_nounits(f_flat, in_pvals)
    # all outputs should be knowns. If this fails
    # the user is creating variables that depend on a
    # argument that was passed as a ShapeDtypeStruct.
    out_flat = []
    for pv, const in out_pvals:
      if pv is None:
        # const is the actual value of the known output
        out_flat.append(const)
      else:
        raise errors.LazyInitError(pv)
    return jax.tree_util.tree_unflatten(out_tree(), out_flat)

  return wrapper


def lazy_init(
  fn: Callable[..., Any],
  mutable: CollectionFilter = True,
  flags: Mapping | None = None,
) -> Callable[..., Any]:
  """Functionalizes a `Scope` function for lazy initialization.

  Similar to ``init`` except that the init function now accepts
  ``jax.ShapeDtypeStruct`` instances for arguments that do not
  affect the variable initialization (typically this is all the input data).

  Example::

    def f(scope, x):
        # the kernel init only uses the shape of x so we don't actually
        # need a value for x and can pass it as a ShapeDtypeStruct in lazy_init.
        k = scope.param("kernel", nn.initializers.lecun_normal(), (x.shape[-1], x.shape[-1]))
        return x @ k
    init_fn = lazy_init(f)
    variables = init_fn(random.key(0), jax.ShapeDtypeStruct((1, 128), jnp.float32))


  Args:
    fn: a function taking a `Scope` as its first argument.
    mutable: the filter determining which variable collections are mutable.
    flags: internal flags.

  Returns:
    `fn` with the scope partially applied. Unlike ``init`` which returns a tuple of function
    output and variables, the lazy init function only returns the variables.
  """
  return partial_eval.lazy_init(
    lambda *args, **kwargs: init(fn, mutable, flags)(*args, **kwargs)[1]
  )


def lazy_init(fn: Module | tp.Callable[..., tp.Any], *args, **kwargs):
  """To run through an arbitrary nnx.Module method and initialize all its needed state.

  Here used to trigger initialization of all `LinenToNNX` module variables."""
  if isinstance(fn, Module):
    module = fn
    assert callable(fn)
  else:
    if not (hasattr(fn, '__self__') and isinstance(fn.__self__, Module)):
      raise ValueError(f'{fn = } needs to be a method of an NNX Module.')
    module = fn.__self__
  _set_initializing(module, True)
  try:
    _ = fn(*args, **kwargs)
  finally:
    _set_initializing(module, False)
  return fn

