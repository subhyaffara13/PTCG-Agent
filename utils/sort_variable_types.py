
def sort_variable_types(types: tp.Iterable[type]):
  def _variable_parents_count(t: type):
    return sum(1 for p in t.mro() if issubclass(p, variablelib.Variable))
  parent_count = {t: _variable_parents_count(t) for t in types}
  return sorted(types, key=lambda t: -parent_count[t])

