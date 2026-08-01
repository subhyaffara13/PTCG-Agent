
def from_hashable_index(idx: HashableIndex) -> Index:
  return tuple([slice(s[0], s[1], s[2]) for s in idx])

