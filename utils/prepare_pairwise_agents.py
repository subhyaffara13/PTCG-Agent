
def prepare_pairwise_agents(villager_roles, werewolf_roles, player_a_config, player_b_config, player_ids):
    pid_v, pid_w = player_ids[: len(villager_roles)], player_ids[len(villager_roles) :]
    agents_v = assign_roles_dup_agents(villager_roles, player_a_config, pid_v)
    agents_w = assign_roles_dup_agents(werewolf_roles, player_b_config, pid_w)
    agents = agents_v + agents_w
    return agents

