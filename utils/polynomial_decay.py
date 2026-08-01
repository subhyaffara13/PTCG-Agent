
def polynomial_decay(step_size, decay_steps, final_step_size, power=1.0):
  def schedule(step_num):
    step_num = jnp.minimum(step_num, decay_steps)
    step_mult = (1 - step_num / decay_steps) ** power
    return step_mult * (step_size - final_step_size) + final_step_size

  return schedule

