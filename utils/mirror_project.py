
def mirror_project(dist, y):
  """Project variables onto their feasible sets (softmax for dist).

  Args:
    dist: 1-d np.array, current estimate of nash distribution
    y: 1-d np.array (same shape as dist), current estimate of payoff gradient
  Returns:
    projected variables (dist, y) as tuple
  """
  dist = special.softmax(dist)
  y = np.clip(y, 0., np.inf)

  return dist, y


def mirror_project(dist, y):
  """Project variables onto their feasible sets (softmax for dist).

  Args:
    dist: 1-d np.array, current estimate of nash distribution
    y: 1-d np.array (same shape as dist), current estimate of payoff gradient
  Returns:
    projected variables (dist, y) as tuple
  """
  dist = special.softmax(dist)
  y = np.clip(y, 0., np.inf)

  return dist, y


def mirror_project(dist, y):
  """Project variables onto their feasible sets (softmax for dist).

  Args:
    dist: 1-d np.array, current estimate of nash distribution
    y: 1-d np.array (same shape as dist), current estimate of payoff gradient
  Returns:
    projected variables (dist, y) as tuple
  """
  dist = special.softmax(dist)
  y = np.clip(y, 0., np.inf)

  return dist, y


def mirror_project(dist, y):
  """Project variables onto their feasible sets (softmax for dist).

  Args:
    dist: 1-d np.array, current estimate of nash distribution
    y: 1-d np.array (same shape as dist), current estimate of payoff gradient
  Returns:
    projected variables (dist, y) as tuple
  """
  dist = special.softmax(dist)
  y = np.clip(y, 0., np.inf)

  return dist, y


def mirror_project(dist):
  """Project variables onto their feasible sets (softmax for dist).

  Args:
    dist: 1-d np.array, current estimate of nash distribution
  Returns:
    projected variables (dist,) as tuple
  """
  dist = special.softmax(dist)

  return (dist,)

