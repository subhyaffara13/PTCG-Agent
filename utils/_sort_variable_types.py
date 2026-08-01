
def _sort_variable_types(types: tp.Iterable[type]) -> list[type]:
  def _variable_parents_count(t: type):
    return sum(1 for p in t.mro() if issubclass(p, variablelib.Variable))

  type_sort_key = {t: (-_variable_parents_count(t), t.__name__) for t in types}
  return sorted(types, key=lambda t: type_sort_key[t])

