
def train_test_split(roshambo_bot_ids):
  """Create a train/test split for the roshambo bots."""

  if FIXED_POPULATION is not None:
    training_ids = FIXED_POPULATION[:]
    testing_ids = FIXED_POPULATION[:]
  elif FLAGS.pop_only >= 0:
    # If the pop_only flag is set, make a population of just that member
    assert FLAGS.pop_only < len(roshambo_bot_ids)
    training_ids = [FLAGS.pop_only]
    testing_ids = [FLAGS.pop_only]
  else:
    # Otherwise, do the train/test split
    bot_ids_copy = roshambo_bot_ids.copy()
    training_ids = list(bot_ids_copy.values())
    testing_ids = []
    if FLAGS.leave_out_set_size == 0:
      testing_ids = training_ids[:]
    else:
      while len(testing_ids) < FLAGS.leave_out_set_size:
        idx = np.random.randint(0, len(training_ids))
        testing_ids.append(training_ids[idx])
        training_ids.pop(idx)
  return training_ids, testing_ids

