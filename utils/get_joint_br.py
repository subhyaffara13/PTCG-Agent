
def get_joint_br(game, weights, mus):
  br_value = jbr.JointBestResponse(game, mus, weights)
  greedy_pi = greedy_policy.GreedyPolicy(game, None, br_value)
  return greedy_pi, br_value

