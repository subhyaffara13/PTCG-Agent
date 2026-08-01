
def ir_consts(consts, avals: Sequence[core.AbstractValue]) -> list[IrValues]:
  uniq_consts = {
      id(c): _ir_constant(c, aval=aval) for c, aval in zip(consts, avals)
  }
  return [uniq_consts[id(c)] for c in consts]

