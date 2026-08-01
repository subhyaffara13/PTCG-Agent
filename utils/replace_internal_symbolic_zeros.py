
def replace_internal_symbolic_zeros(
    x: JaxTypeOrTracer | Zero) -> JaxTypeOrTracer | SymbolicZero:
  return SymbolicZero(x.aval) if type(x) is Zero else x

