
def aval_mismatch_extra(a1: AbstractValue, a2: AbstractValue) -> str:
  assert not typematch(a1, a2)
  if isinstance(a1, ShapedArray) and isinstance(a2, ShapedArray):
    mismatches = []
    if a1.dtype != a2.dtype:
      mismatches.append('the dtypes do not match')
    if a1.shape != a2.shape:
      mismatches.append('the shapes do not match')
    if a1.mat != a2.mat:
      mismatches.append('the manual axis types do not match')
    # TODO(yashkatariya,mattjj): add check for sharding-in-types mismatch

    if len(mismatches) == 0:
      return ''
    elif len(mismatches) == 1:
      return ', so ' + mismatches[0]
    else:
      return ', so ' + ', '.join(mismatches[:-1]) + ', and ' + mismatches[-1]
  return ''

