
def _cached_lowering_miss(
    ctx: ModuleContext,
    eqn: core.JaxprEqn,
    cache_key: LoweringCacheKey,
    avals_in: tuple[core.AbstractValue, ...],
    **params,
) -> LoweringCacheValue:
  """Lowers a jaxpr equation and populates the cache.

  The jaxpr equation's lowering is emitted as an out-of-line MLIR function, and
  that function's construction is cached in the event that we see a similar
  equation. For each such equation we either inline the function body or emit
  an out-of-line call to it, depending on whether any of the lowering rules
  opted out of inlining."""
  ordered_effects = (tuple(effects_lib.ordered_effects.filter_in(eqn.effects))
                     if eqn.effects else ())
  platform_rules, default_rule, inline = _get_lowering_rules(
      ctx, eqn.primitive, eqn.ctx)
  with (source_info_util.user_context(eqn.source_info.traceback),
        eqn.ctx.manager):
    avals_out = map(lambda v: v.aval, eqn.outvars)
    cache_entry = _emit_lowering_rule_as_fun(
        partial(_uncached_lowering, eqn.primitive, eqn.ctx, eqn.effects,
                platform_rules, default_rule),
        ctx, eqn.ctx, eqn.primitive, ordered_effects, avals_in, avals_out,
        inline, **params,
    )
    ctx.lowering_cache[cache_key] = cache_entry
    return cache_entry

