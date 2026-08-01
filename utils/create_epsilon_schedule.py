
def create_epsilon_schedule(sched_str):
  """Creates an epsilon schedule from the string as desribed in the flags."""
  values = FLAGS.epsilon_schedule.split(",")
  if values[0] == "linear":
    assert len(values) == 4
    return rl_tools.LinearSchedule(
        float(values[1]), float(values[2]), int(values[3]))
  elif values[0] == "constant":
    assert len(values) == 2
    return rl_tools.ConstantSchedule(float(values[1]))
  else:
    print("Unrecognized schedule string: {}".format(sched_str))
    sys.exit()

