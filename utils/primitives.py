
def primitives(jaxpr: core.Jaxpr):
  return histogram(jaxpr, lambda eqn: eqn.primitive.name)

