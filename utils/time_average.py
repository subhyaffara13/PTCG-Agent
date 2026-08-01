
def time_average(traj):
  """Time-averaged population state trajectory.

  Args:
    traj: Trajectory as `numpy.ndarray`. Time is along the first dimension,
      types/strategies along the second.

  Returns:
    Time-averaged trajectory.
  """
  n = traj.shape[0]
  sum_traj = np.cumsum(traj, axis=0)
  norm = 1. / np.arange(1, n + 1)
  return sum_traj * norm[:, np.newaxis]

