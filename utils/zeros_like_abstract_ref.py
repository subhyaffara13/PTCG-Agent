
def zeros_like_abstract_ref(aval: AbstractRef) -> core.Ref:
  val = ad_util.zeros_like_aval(aval.inner_aval)
  return core.new_ref(val)

