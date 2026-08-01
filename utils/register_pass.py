
def register_pass(pass_: Pass):
  if pass_.name in _pass_registry:
    raise ValueError(f"Pass {pass_.name} already registered")
  _pass_registry[pass_.name] = pass_

