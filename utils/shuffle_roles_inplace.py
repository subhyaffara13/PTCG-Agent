
def shuffle_roles_inplace(config):
    agents = config["agents"]
    roles = [agent["role"] for agent in agents]
    random.shuffle(roles)
    for new_role, agent in zip(roles, agents):
        agent["role"] = new_role

