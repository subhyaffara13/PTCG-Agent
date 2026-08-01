
def _pytree_key_as_tree_key(key: PyTreeKey) -> TreeKey:
  match key:
    case (jtu.SequenceKey(idx=k)
          | jtu.DictKey(key=k)
          | jtu.FlattenedIndexKey(key=k)
          | jtu.GetAttrKey(name=k)):
      return k  # pytype: disable=bad-return-type
  raise KeyError(f'Cannot convert unexpected PyTreeKey to TreeKey: {key!r}')

