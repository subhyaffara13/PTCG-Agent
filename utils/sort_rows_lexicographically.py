
def sort_rows_lexicographically(array):
  """Returns a numpy array with lexicographic-ordered rows.

  This function can be used to check that 2 Heuristic Payoff Tables are equal,
  by normalizing them using a fixed ordering of the rows.

  Args:
    array: The 2D numpy array to sort by rows.
  """
  return np.array(sorted(array.tolist()))

