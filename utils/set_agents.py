
def set_agents(agent_matrix, map_matrix):
    # check input sizes
    if agent_matrix.shape != map_matrix.shape:
        raise ValueError("Agent configuration and map matrix have mis-matched sizes")

    agents = []
    xs, ys = agent_matrix.shape
    for i in range(xs):
        for j in range(ys):
            n_agents = agent_matrix[i, j]
            if n_agents > 0:
                if map_matrix[i, j] == -1:
                    raise ValueError(
                        "Trying to place an agent into a building: check map matrix and agent configuration"
                    )
                agent = DiscreteAgent(xs, ys, map_matrix)
                agent.set_position(i, j)
                agents.append(agent)
    return agents

