
def _simple_entrystr(key: KeyEntry) -> str:
  match key:
    case (
        SequenceKey(idx=key)
        | DictKey(key=key)
        | GetAttrKey(name=key)
        | FlattenedIndexKey(key=key)
    ):
      return str(key)
    case _:
      return str(key)

