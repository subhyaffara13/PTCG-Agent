
def shuffle_roles(agents_config, seed):
    roles_config = [{"role": agent["role"], "role_params": agent.get("role_params", {})} for agent in agents_config]
    permuted_roles_config = get_permutation(roles_config, seed)
    new_agents_config = deepcopy(agents_config)
    for role, agent in zip(permuted_roles_config, new_agents_config):
        agent["role"] = role["role"]
        agent["role_params"] = role["role_params"]
    return new_agents_config

