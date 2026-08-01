
def _try_two_solvers(func, *args, **kwargs):
  try:
    logging.debug("Trying CVXOPT.")
    kwargs_ = {"solver_kwargs": DEFAULT_CVXOPT_SOLVER_KWARGS, **kwargs}
    res = func(*args, **kwargs_)
  except:  # pylint: disable=bare-except
    logging.debug("CVXOPT failed. Trying OSQP.")
    kwargs_ = {"solver_kwargs": DEFAULT_OSQP_SOLVER_KWARGS, **kwargs}
    res = func(*args, **kwargs_)
  return res

