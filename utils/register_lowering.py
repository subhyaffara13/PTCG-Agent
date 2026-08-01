
def register_lowering(
    aten_fn,
    broadcast=False,
    type_promotion_kind: ELEMENTWISE_TYPE_PROMOTION_KIND
    | None = ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
    convert_input_to_bool=False,
    lowering_dict=lowerings,
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    """
    Shim to support decorator syntax.
    """
    return functools.partial(
        _register_lowering,
        aten_fn,
        broadcast=broadcast,
        type_promotion_kind=type_promotion_kind,
        convert_input_to_bool=convert_input_to_bool,
        lowering_dict=lowering_dict,
    )


def register_lowering(prim: core.Primitive, rule: LoweringRule,
                      platform: str | None = None, inline: bool = True,
                      cacheable: bool = True) -> None:
  """Registers a lowering rule for a primitive.

  Args:
    prim: The primitive to register the rule for.
    rule: The lowering rule to register.
    platform: The platform to register the rule for. If None, this is a common
      rule applicable to all platforms. Platform-specific rules take precedence
      over common rules.
    inline: Whether to emit the lowering inline. If False, the lowering will be
      emitted in a separate function, called by similar instances of the
      lowering.
    uncacheable: Whether this primitive's lowering can be cached. This is a
      temporary flag that will be removed after primitives that have problems
      with caching are fixed.
  """
  assert not isinstance(rule, LoweringRuleEntry)
  if not cacheable:
    _uncacheable_primitives.add(prim)
  if platform is None:
    _lowerings[prim] = LoweringRuleEntry(rule, inline)
  else:
    if not xb.is_known_platform(platform):
      known_platforms = sorted(xb.known_platforms())
      raise NotImplementedError(
          f"Registering an MLIR lowering rule for primitive {prim}"
          f" for an unknown platform {platform}. Known platforms are:"
          f" {', '.join(known_platforms)}.")
    # For backward compatibility reasons, we allow rules to be registered
    # under "gpu" even though the platforms are now called "cuda" and "rocm".
    # TODO(phawkins): fix up users to specify either "cuda" or "rocm" and remove
    # this expansion.
    for p in xb.expand_platform_alias(platform):
      _platform_specific_lowerings[p][prim] = LoweringRuleEntry(rule, inline)


def register_lowering(primitive: jax_core.Primitive) -> Callable[[_T], _T]:
  def wrapper(fn):
    triton_lowering_rules[primitive] = fn
    return fn
  return wrapper

