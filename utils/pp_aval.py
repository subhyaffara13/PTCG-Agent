
def pp_aval(a: AbstractValue, context: JaxprPpContext) -> str:
  return a.str_short(short_dtypes=True)

