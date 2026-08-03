import os
import random

def generate_game_tasks(output_dir, num_blocks, config, use_random_agents, debug, shuffle_player_ids):
    """
    Generates all game configurations for the entire experiment.
    """
    base_game_config = config["game_config"]
    players_data = base_game_config["agents"]
    base_role_configs = [{"role": agent["role"], "role_params": agent.get("role_params", {})} for agent in players_data]

    logger.info("Generating all unique role configurations...")
    all_role_configs = get_all_unique_role_configs(base_role_configs)
    logger.info(f"Found {len(all_role_configs)} unique arrangements.")

    available_role_configs = []

    for block_index in range(num_blocks):
        block_dir = os.path.join(output_dir, f"block_{block_index}")
        os.makedirs(block_dir, exist_ok=True)

        if not available_role_configs:
            if num_blocks > len(all_role_configs):
                logger.warning("Sampling with replacement as num_blocks > unique configurations.")
            available_role_configs = list(all_role_configs)
            random.shuffle(available_role_configs)

        block_role_config = available_role_configs.pop()
        random.shuffle(players_data)
        current_players_deque = collections.deque(players_data)

        for game_in_block in range(len(players_data)):
            game_dir = os.path.join(block_dir, f"game_{game_in_block}")
            os.makedirs(game_dir, exist_ok=True)

            current_players = list(current_players_deque)
            game_agents_config = [
                {**player_config, **block_role_config[i]} for i, player_config in enumerate(current_players)
            ]

            if shuffle_player_ids:
                player_ids = [agent["id"] for agent in game_agents_config]
                random.shuffle(player_ids)
                for i, agent in enumerate(game_agents_config):
                    agent["id"] = player_ids[i]

            game_config = {**base_game_config, "agents": game_agents_config}
            yield (game_dir, game_config, use_random_agents, debug, block_index, game_in_block)
            current_players_deque.rotate(1)


def generate_game_tasks(output_dir, num_tournaments, config, use_random_agents, debug):
    """
    Generates game configurations for a pairwise matrix tournament.
    """
    base_game_config = config["game_config"]
    all_players = base_game_config["agents"]
    num_players = len(all_players)
    base_roles = [agent["role"] for agent in all_players]
    player_ids = [agent["id"] for agent in all_players]

    villager_roles, werewolf_roles = get_team_roles(base_roles)

    if not werewolf_roles:
        raise ValueError("Configuration must include at least one werewolf role.")
    if not villager_roles:
        raise ValueError("Configuration must include at least one villager role.")

    for tourney_idx in range(num_tournaments):
        for i in range(num_players):
            for j in range(num_players):
                game_dir = os.path.join(output_dir, f"tourney_{tourney_idx}", f"game_{i}_vs_{j}")
                os.makedirs(game_dir, exist_ok=True)

                player_a_config = all_players[i]
                player_b_config = all_players[j]

                game_agents_config = prepare_pairwise_agents(
                    villager_roles, werewolf_roles, player_a_config, player_b_config, player_ids
                )

                # since name has to be unique and all names come from config, we by default shuffle all names
                # since name might change
                random.shuffle(player_ids)
                for agent_ind, agent in enumerate(game_agents_config):
                    agent["id"] = player_ids[agent_ind]

                random.shuffle(game_agents_config)

                game_config = {**base_game_config, "agents": game_agents_config}
                yield game_dir, game_config, use_random_agents, debug, tourney_idx, f"{i}_vs_{j}"


def generate_game_tasks(args, run_output_dir, agent_pool, game_config_template):
    """Generates configurations for each game to be run."""
    original_agents_config = game_config_template.get("agents", [])
    num_agents_per_game = len(original_agents_config)

    if num_agents_per_game == 0:
        logger.error("The base game config must specify a list of agents with roles.")
        return []

    if args.without_replacement:
        if num_agents_per_game > len(agent_pool):
            logger.error(
                f"Cannot sample {num_agents_per_game} agents without replacement "
                f"from a pool of only {len(agent_pool)} agents."
            )
            return []
        logger.info("Sampling agents without replacement.")
    else:
        logger.info("Sampling agents with replacement.")

    role_configs = [
        {"role": agent["role"], "role_params": agent.get("role_params")} for agent in original_agents_config
    ]

    game_tasks = []
    for i in range(args.num_games):
        game_dir = os.path.join(run_output_dir, f"game_{i}")
        os.makedirs(game_dir, exist_ok=True)

        if args.shuffle_roles:
            random.shuffle(role_configs)

        if args.without_replacement:
            sampled_agent_specs = random.sample(agent_pool, k=num_agents_per_game)
        else:
            sampled_agent_specs = random.choices(agent_pool, k=num_agents_per_game)

        new_agents_config = []
        for j, original_agent in enumerate(original_agents_config):
            sampled_spec = sampled_agent_specs[j]
            role_config = role_configs[j]
            role_params = role_config.get("role_params") or {}
            new_agent = {
                **sampled_spec,
                "role": role_config["role"],
                "id": original_agent["id"],
                "role_params": role_params,
            }
            new_agents_config.append(new_agent)

        if args.shuffle_player_ids:
            player_ids = [agent["id"] for agent in new_agents_config]
            random.shuffle(player_ids)
            for agent, player_id in zip(new_agents_config, player_ids):
                agent["id"] = player_id

        final_game_config = {**game_config_template, "agents": new_agents_config}
        game_tasks.append((game_dir, final_game_config, args.use_random_agents, args.debug))

    return game_tasks

