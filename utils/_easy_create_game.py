
def _easy_create_game():
  """Uses the helper function to create the same game as above."""
  return pyspiel.create_matrix_game("matching_pennies", "Matching Pennies",
                                    ["Heads", "Tails"], ["Heads", "Tails"],
                                    [[-1, 1], [1, -1]], [[1, -1], [-1, 1]])

