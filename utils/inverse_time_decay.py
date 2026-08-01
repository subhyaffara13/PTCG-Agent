
def inverse_time_decay(step_size, decay_steps, decay_rate, staircase=False):
  if staircase:
    def schedule(i):
      return step_size / (1 + decay_rate * jnp.floor(i / decay_steps))
  else:
    def schedule(i):
      return step_size / (1 + decay_rate * i / decay_steps)
  return schedule

