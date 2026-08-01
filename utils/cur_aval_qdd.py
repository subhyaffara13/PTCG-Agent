
def cur_aval_qdd(x):
  aval = typeof(x)
  qdd = cur_qdd(x) if aval.has_qdd else None
  return AvalQDD(aval, qdd)

