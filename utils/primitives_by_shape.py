
def primitives_by_shape(jaxpr: core.Jaxpr):
  def shape_fmt(var):
    return '*' if isinstance(var, core.DropVar) else var.aval.str_short()
  def key(eqn):
    return (eqn.primitive.name, ' '.join(map(shape_fmt, eqn.outvars)))
  return histogram(jaxpr, key, ' :: '.join)

