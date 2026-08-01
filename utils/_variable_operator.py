
def _variable_operator(name: str) -> tp.Callable[[Variable[A], tp.Any], A]:
  def variable_operator_method(self, other):
    value = self.get_value()
    if isinstance(other, Variable):
      other = other.get_value()
    return getattr(value, name)(other)

  variable_operator_method.__name__ = name
  return variable_operator_method

