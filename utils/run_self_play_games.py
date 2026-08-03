import copy
import os
import random

def run_self_play_games(
    model_name,
    thumbnail,
    output_dir,
    num_games,
    config,
    use_random_agents,
    debug,
    parallel,
    num_processes,
    shuffle_roles,
):
    """
    Generates and runs game tasks for the self-play experiment.
    """
    if debug:
        logger.warning("Debug mode is enabled. Forcing sequential execution.")

    game_tasks = []
    base_game_config = config["game_config"]

    # modify the config to use a single model
    agents = base_game_config["agents"]
    for agent in agents:
        agent["thumbnail"] = thumbnail
        agent["agent_id"] = f"llm/{model_name}"
        agent["display_name"] = os.path.basename(model_name)
        agent["llms"][0]["model_name"] = model_name

    for i in range(num_games):
        game_output_dir = os.path.join(output_dir, f"game_{i}")
        os.makedirs(game_output_dir, exist_ok=True)

        game_config = copy.deepcopy(base_game_config)

        if shuffle_roles:
            logger.info(f"Shuffling roles for game {i}")
            role_configs = [
                {"role": agent["role"], "role_params": agent.get("role_params", {})} for agent in game_config["agents"]
            ]
            random.shuffle(role_configs)
            for agent, role_config in zip(game_config["agents"], role_configs):
                agent["role"] = role_config["role"]
                agent["role_params"] = role_config["role_params"]

        # shuffle player ids
        logger.info(f"Shuffling player ids for game {i}")
        shuffle_field(game_config["agents"], "id")

        task = (game_output_dir, game_config, use_random_agents, debug)
        game_tasks.append(task)

    with tqdm(total=num_games, desc="Running Self-Play Games") as pbar:
        if parallel:
            with ThreadPoolExecutor(max_workers=num_processes) as executor:
                futures = [executor.submit(game_runner_wrapper, task) for task in game_tasks]
                for future in as_completed(futures):
                    # You could also add error handling here by checking future.exception()
                    pbar.update(1)
        else:
            for task in game_tasks:
                game_runner_wrapper(task)
                pbar.update(1)

