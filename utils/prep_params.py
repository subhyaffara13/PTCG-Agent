
def prep_params(dist, pt, num_params):
  params = [dist]
  if num_params > 1:
    num_players = len(dist)
    nabla = [misc.pt_reduce(pt[i], dist, [i]) for i in range(num_players)]
    params += [nabla]  # policy_gradient
  return tuple(params)


def prep_params(dist, payoff_matrices, num_params, solver_tuple):
  params = [dist]
  if num_params > 1:
    params += [payoff_matrices[0].dot(params[0])]  # policy_gradient
  if num_params > 2:
    params += [np.linalg.norm(params[1], ord=solver_tuple[1])]
  return tuple(params)

