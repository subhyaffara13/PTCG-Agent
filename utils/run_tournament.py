import random

def run_tournament(output_dir, num_tournaments, config, use_random_agents, debug, parallel, num_processes):
    """
    Runs a tournament by generating all game tasks and processing them,
    potentially in parallel.
    """
    total_games = num_tournaments * len(config["game_config"]["agents"]) ** 2

    if parallel:
        logger.info(f"Running games in parallel with up to {num_processes} processes.")

    game_tasks = generate_game_tasks(output_dir, num_tournaments, config, use_random_agents, debug)

    # the following shuffle is to reduce the load of a particular LLM api
    game_tasks = [*game_tasks]
    random.shuffle(game_tasks)

    with tqdm(total=total_games, desc="Processing Games") as pbar:
        if parallel:
            with multiprocessing.Pool(processes=num_processes) as pool:
                for _ in pool.imap_unordered(game_runner_wrapper, game_tasks):
                    pbar.update(1)
        else:
            for task_args in game_tasks:
                game_runner_wrapper(task_args)
                pbar.update(1)

    logger.info("All game tasks have been processed.")

