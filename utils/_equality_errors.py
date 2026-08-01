
def _equality_errors(path, t1, t2, is_leaf):
  # If both are leaves, this isn't a structure equality error.
  if (treedef_is_strict_leaf(tree_structure(t1, is_leaf=is_leaf)) and
      treedef_is_strict_leaf(tree_structure(t2, is_leaf=is_leaf))): return

  # The trees may disagree because they are different types:
  if type(t1) != type(t2):
    yield path, str(type(t1)), str(type(t2)), 'their Python types differ'
    return  # no more errors to find

  # Or they may disagree because their roots have different numbers or keys of
  # children (with special-case handling of list/tuple):
  if isinstance(t1, (list, tuple)):
    assert type(t1) == type(t2)
    if len(t1) != len(t2):
      yield (path,
             f'{type(t1).__name__} of length {len(t1)}',
             f'{type(t2).__name__} of length {len(t2)}',
             'the lengths do not match')
      return  # no more errors to find
  t1_children, t1_meta = flatten_one_level(t1)
  t2_children, t2_meta = flatten_one_level(t2)
  t1_children = tuple(t1_children)
  t2_children = tuple(t2_children)
  t1_keys, t2_keys = _child_keys(t1), _child_keys(t2)
  try:
    diff = ' '.join(repr(k.key) for k in
                    set(t1_keys).symmetric_difference(set(t2_keys)))
  except:
    diff = ''
  if len(t1_children) != len(t2_children):
    yield (path,
           f'{type(t1)} with {len(t1_children)} child'
           f'{"ren" if len(t1_children) > 1 else ""}',
           f'{type(t2)} with {len(t2_children)} child'
           f'{"ren" if len(t2_children) > 1 else ""}',
           'the numbers of children do not match' +
           (diff and f', with the symmetric difference of key sets: {{{diff}}}')
           )
    return  # no more errors to find

  # Or they may disagree if their roots have different pytree metadata:
  if t1_meta != t2_meta:
    yield (path,
           f'{type(t1)} with pytree metadata {t1_meta}',
           f'{type(t2)} with pytree metadata {t2_meta}',
           'the pytree node metadata does not match')
    return  # no more errors to find

  # If the root types and numbers of children agree, there must be a mismatch in
  # a subtree, so recurse:
  assert t1_keys == t2_keys, \
      f"equal pytree nodes gave different tree keys: {t1_keys} and {t2_keys}"
  for k, c1, c2 in zip(t1_keys, t1_children, t2_children):
    yield from _equality_errors((*path, k), c1, c2, is_leaf)

