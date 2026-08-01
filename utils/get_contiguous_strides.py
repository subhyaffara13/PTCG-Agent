
def get_contiguous_strides(xs):
  strides_ret = []
  stride = 1
  for x in xs[::-1]:
    strides_ret.append(stride)
    stride *= x
  return strides_ret[::-1]

