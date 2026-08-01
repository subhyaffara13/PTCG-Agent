
def ToShortestFloat(original):
  """Returns the shortest float that has same value in wire."""
  # All 4 byte floats have between 6 and 9 significant digits, so we
  # start with 6 as the lower bound.
  # It has to be iterative because use '.9g' directly can not get rid
  # of the noises for most values. For example if set a float_field=0.9
  # use '.9g' will print 0.899999976.
  precision = 6
  rounded = float('{0:.{1}g}'.format(original, precision))
  while TruncateToFourByteFloat(rounded) != original:
    precision += 1
    rounded = float('{0:.{1}g}'.format(original, precision))
  return rounded

