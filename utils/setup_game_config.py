import random

def setup_game_config(max_turns: int, base_config: dict, model_name: str):
    """
    Sets up the game configuration for a single run.
    """
    config = base_config.copy()

    # Define roles and shuffle them
    roles = ["Werewolf", "Werewolf", "Doctor", "Seer", "Villager", "Villager", "Villager", "Villager"]
    random.shuffle(roles)
    random.shuffle(AGENT_NAMES)

    # Create agent configurations
    agents_config = []
    for i, role in enumerate(roles):
        player_name = AGENT_NAMES[i]
        agents_config.append(
            {
                "role": role,
                "id": player_name,
                "agent_id": f"llm/{model_name}",
                "display_name": f"{model_name}/{player_name}",
                "agent_harness_name": "llm_harness",
                "chat_mode": "text",
                "llms": [{"model_name": model_name}],
            }
        )

    config["agents"] = agents_config

    # Update discussion protocol with the specified max_turns
    if "discussion_protocol" in config and config["discussion_protocol"]["name"] == "TurnByTurnBiddingDiscussion":
        config["discussion_protocol"]["params"]["max_turns"] = max_turns
    else:
        logger.warning("Could not find 'TurnByTurnBiddingDiscussion' protocol to set max_turns.")

    # Set a new random seed for each game to ensure role/name shuffling is different
    config["seed"] = random.randint(0, 2**32 - 1)

    agent_harnesses = [f"llm/{model_name}"] * len(roles)

    return config, agent_harnesses

