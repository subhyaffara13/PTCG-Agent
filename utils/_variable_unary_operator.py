
def _variable_unary_operator(name: str) -> tp.Callable[[Variable[A]], A]:
  def variable_unary_operator_method(self):
    value = self.get_value()
    return getattr(value, name)()

  variable_unary_operator_method.__name__ = name
  return variable_unary_operator_method

