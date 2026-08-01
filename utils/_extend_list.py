
def _extend_list(ls, idx, nextvalue):
  assert idx <= len(ls)
  if idx == len(ls):
    ls.append(nextvalue)
  return ls

