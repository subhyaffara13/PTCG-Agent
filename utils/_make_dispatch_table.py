
def _make_dispatch_table(
    name: str, **tables: Sequence[_Extern | _Fallback]
) -> Callable[..., ir.Value]:

  def inner(
      ctx: LoweringRuleContext, *args: ir.Value, **_
  ) -> ir.Value:
    table = tables[ctx.context.platform]
    h = next((e for e in table if e.matches(ctx.avals_in)), None)
    if h is None:
      arg_aval_dtypes = tuple(aval.dtype for aval in ctx.avals_in)
      raise NotImplementedError(
          f"unsupported types for {name}: {arg_aval_dtypes}"
      )
    return h.lower(ctx, *args)

  return inner

