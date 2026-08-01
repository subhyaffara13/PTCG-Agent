
def source_locations(jaxpr: core.Jaxpr):
  def key(eqn):
    return source_info_util.summarize(eqn.source_info)
  return histogram(jaxpr, key)

