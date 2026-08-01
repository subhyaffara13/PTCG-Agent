
def replace_rule_output_symbolic_zeros(
    x: JaxTypeOrTracer | SymbolicZero) -> JaxTypeOrTracer | Zero:
  return Zero(x.aval) if type(x) is SymbolicZero else x

