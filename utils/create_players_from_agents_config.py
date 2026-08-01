
def create_players_from_agents_config(
    agents_config: List[Dict], randomize_roles: bool = False, randomize_ids: bool = False, seed: Optional[int] = None
) -> List[Player]:
    if randomize_roles:
        assert seed is not None
        agents_config = shuffle_roles(agents_config, seed)

    if randomize_ids:
        assert seed is not None
        # Note that we have to use a different seed for shuffle_ids vs shuffle_roles, otherwise the ids and roles
        # arrangement will remain the same. Also, using different seed (even just a simple arithmatic addition),
        # LCG ensures that the sequence of random numbers will be uncorrelated.
        agents_config = shuffle_ids(agents_config, seed + 123)

    # check all agents have unique ids
    agent_ids = [agent_config["id"] for agent_config in agents_config]
    if len(agent_ids) != len(set(agent_ids)):
        counts = Counter(agent_ids)
        duplicates = [item for item, count in counts.items() if count > 1 and item is not None]
        if duplicates:
            raise ValueError(f"Duplicate agent ids found: {', '.join(duplicates)}")
    agents = [Agent(**agent_config) for agent_config in agents_config]
    players = [
        Player(id=agent.id, agent=agent, role=ROLE_CLASS_MAP[agent.role](**agent.role_params)) for agent in agents
    ]
    return players

