
def same_referent(x: Any, y: Any) -> bool:
  return get_referent(x) is get_referent(y)

