
def _while_is_high(*_, cond_jaxpr, body_jaxpr, **__):
  return cond_jaxpr.is_high or body_jaxpr.is_high

