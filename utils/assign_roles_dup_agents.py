
def assign_roles_dup_agents(roles, agent_config, player_ids):
    agents = [deepcopy(agent_config) for _ in range(len(roles))]
    for role, agent, player_id in zip(roles, agents, player_ids):
        agent["role"] = role
        agent["id"] = player_id
    return agents

