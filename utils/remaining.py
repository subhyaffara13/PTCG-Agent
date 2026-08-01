
def remaining(original, *removed_lists):
  removed = set(itertools.chain(*removed_lists))
  return [i for i in original if i not in removed]

