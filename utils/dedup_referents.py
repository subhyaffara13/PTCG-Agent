
def dedup_referents(itr: Iterable[Any]) -> list[Any]:
  return list({HashableWrapper(get_referent(x)):x for x in itr}.values())

