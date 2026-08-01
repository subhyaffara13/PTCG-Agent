
def dilated_dgf_divergence(mmd_1, mmd_2):
  """Bregman divergence between two MMDDilatedEnt objects.

      The value is equivalent to a sum of two Bregman divergences
      over the sequence form, one for each player.

  Args:
      mmd_1: MMDDilatedEnt Object
      mmd_2: MMDDilatedEnt Object

  Returns:
      Scalar.
  """

  dgf_values = [mmd_1.dgf_eval(), mmd_2.dgf_eval()]
  dgf_grads = mmd_2.dgf_grads()
  div = 0
  for player in range(2):
    div += divergence(mmd_1.sequences[player], mmd_2.sequences[player],
                      dgf_values[0][player], dgf_values[1][player],
                      dgf_grads[player])
  return div

