
def pp_effect(effect: Effect, context: JaxprPpContext) -> pp.Doc:
  if hasattr(effect, "_pretty_print"):
    return effect._pretty_print(context)
  return pp.text(str(effect))

