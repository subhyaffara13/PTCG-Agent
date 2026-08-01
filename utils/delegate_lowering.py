
def delegate_lowering(ctx, lowering_fun, *args, **ctx_override_kwargs):
  """Side-effects on `ctx`"""
  ctx_new = ctx.replace(**ctx_override_kwargs)
  out = lowering_fun(ctx_new, *args)
  ctx.set_tokens_out(ctx_new.tokens_out)
  return out

