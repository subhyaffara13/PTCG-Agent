
def remove_epsilon_negative_probs(probs, epsilon=1e-9):
  """Removes negative probabilities that occur due to precision errors."""
  if len(probs[probs < 0]) > 0:  # pylint: disable=g-explicit-length-test
    # Ensures these negative probabilities aren't large in magnitude, as that is
    # unexpected and likely not due to numerical precision issues
    print("Probabilities received were: {}".format(probs[probs < 0]))
    assert np.all(np.min(probs[probs < 0]) > -1.*epsilon), (
        "Negative Probabilities received were: {}".format(probs[probs < 0]))

    probs[probs < 0] = 0
    probs = probs / np.sum(probs)
  return probs

