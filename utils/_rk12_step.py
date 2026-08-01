
def _rk12_step(func, y0, dt):
  """Improved Euler-Integration step to integrate dynamics.

  Args:
    func: Function handle to time derivative.
    y0:   Current state.
    dt:   Integration step.

  Returns:
    Next state.
  """
  dy = func(y0)
  y_ = y0 + dt * dy
  return y0 + dt / 2. * (dy + func(y_))

