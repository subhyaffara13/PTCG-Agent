
def create_agents(
    nagents,
    map_matrix,
    obs_range,
    randomizer,
    flatten=False,
    randinit=False,
    constraints=None,
):
    """Initializes the agents on a map (map_matrix).

    -nagents: the number of agents to put on the map
    -randinit: if True will place agents in random, feasible locations
               if False will place all agents at 0
    expanded_mat: This matrix is used to spawn non-adjacent agents
    """
    xs, ys = map_matrix.shape
    agents = []
    expanded_mat = np.zeros((xs + 2, ys + 2))
    for i in range(nagents):
        xinit, yinit = (0, 0)
        if randinit:
            xinit, yinit = feasible_position_exp(
                randomizer, map_matrix, expanded_mat, constraints=constraints
            )
            # fill expanded_mat
            expanded_mat[xinit + 1, yinit + 1] = -1
            expanded_mat[xinit + 2, yinit + 1] = -1
            expanded_mat[xinit, yinit + 1] = -1
            expanded_mat[xinit + 1, yinit + 2] = -1
            expanded_mat[xinit + 1, yinit] = -1
        agent = DiscreteAgent(
            xs, ys, map_matrix, randomizer, obs_range=obs_range, flatten=flatten
        )
        agent.set_position(xinit, yinit)
        agents.append(agent)
    return agents

