
def _ref_typecompat(a, a_):
  return (isinstance(a, AbstractRef) and
          core.typecompat(a.to_ct_aval().inner_aval, a_))

