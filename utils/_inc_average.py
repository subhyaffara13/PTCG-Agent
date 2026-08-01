
def _inc_average(count, average, value):
  """Computes the incremental average, `a_n = ((n - 1)a_{n-1} + v_n) / n`."""
  count += 1
  average = ((count - 1) * average + value) / count
  return (count, average)

