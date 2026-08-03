import logging

def marl_path_finding_example(_):
  """Example usage of multiagent Nash Q-learner.

  Based on https://www.jmlr.org/papers/volume4/hu03a/hu03a.pdf
  """

  logging.info("Creating the Grid Game")
  env = rl_environment.Environment(
      "pathfinding", grid="B.A\n...\na.b", players=2, step_reward=-1.)

  qlearner = QLearner(0, env.game.num_distinct_actions())
  nashqlearner = MultiagentQLearner(
      1, 2, [env.game.num_distinct_actions()] * 2, TwoPlayerNashSolver()
  )

  time_step = env.reset()
  actions = [None, None]

  while not time_step.last():
    actions = [
        qlearner.step(time_step).action,
        nashqlearner.step(time_step, actions).action
    ]
    time_step = env.step(actions)
    print_iteration(actions, env.get_state)

