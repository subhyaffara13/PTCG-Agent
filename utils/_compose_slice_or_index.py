
def _compose_slice_or_index(slice_or_idx1, slice_or_idx2):
  ret = []
  i = 0
  j = 0
  while True:
    if i == len(slice_or_idx1):
      ret.extend(slice_or_idx2[j:])
      return tuple(ret)
    elif j == len(slice_or_idx2):
      ret.extend(slice_or_idx1[i:])
      return tuple(ret)
    elif isinstance(slice_or_idx1[i], int):
      ret.append(slice_or_idx1[i])
      i += 1
    elif isinstance(slice_or_idx2[j], int):
      ret.append(
          slice_or_idx1[i].start + slice_or_idx2[j] * slice_or_idx1[i].step
      )
      i += 1
      j += 1
    else:
      ret.append(
          slice(
              slice_or_idx1[i].start
              + slice_or_idx2[j].start * slice_or_idx1[i].step,
              slice_or_idx1[i].start
              + slice_or_idx2[j].stop * slice_or_idx1[i].step,
              slice_or_idx1[i].step * slice_or_idx2[j].step,
          )
      )
      i += 1
      j += 1

