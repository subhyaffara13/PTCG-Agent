
def round_maintain_sum(x):
  """Returns element-wise rounded version y of a vector x, with sum(x)==sum(y).

  E.g., if x = array([3.37625333, 2.27920304, 4.34454364]), note sum(x) == 10.
  However, naively doing y = np.round(x) yields sum(y) == 9. In this function,
  however, the rounded counterpart y will have sum(y) == 10.

  Args:
    x: a vector.
  """
  y = np.floor(x)
  sum_diff = round(sum(x)) - sum(y)  # Difference of original vs. floored sum
  indices = np.argsort(y - x)[:int(sum_diff)]  # Indices with highest difference
  y[indices] += 1  # Add the missing mass to the elements with the most missing
  return y

