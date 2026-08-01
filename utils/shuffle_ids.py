
def shuffle_ids(agents_config, seed):
    ids = [agent["id"] for agent in agents_config]
    permuted_ids = get_permutation(ids, seed)
    new_agents_config = deepcopy(agents_config)
    for player_id, agent in zip(permuted_ids, new_agents_config):
        agent["id"] = player_id
    return new_agents_config

