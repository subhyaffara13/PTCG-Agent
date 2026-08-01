
def _move_right(lst, to_move):
  lst, rest = split_list(lst, [len(to_move)])
  left, right = partition_list(to_move, lst)
  return [*left, *right, *rest]

