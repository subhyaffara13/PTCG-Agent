
def typecheck(aval: AbstractValue, x) -> bool:
  return typecompat(aval, typeof(x))

