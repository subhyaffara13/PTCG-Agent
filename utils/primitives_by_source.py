
def primitives_by_source(jaxpr: core.Jaxpr):
  def key(eqn):
    src = source_info_util.summarize(eqn.source_info)
    return (eqn.primitive.name, src)
  return histogram(jaxpr, key, ' @ '.join)

