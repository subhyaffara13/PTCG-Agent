
def run_games(args, game_tasks):
    """Executes the generated game tasks, either sequentially or in parallel."""
    logger.info(f"Generated {len(game_tasks)} game tasks.")
    if args.parallel:
        num_processes = args.num_processes or max(1, math.floor(multiprocessing.cpu_count() * 0.8))
        logger.info(f"Running games in parallel with up to {num_processes} processes.")
        with tqdm(total=len(game_tasks), desc="Processing Games") as pbar:
            with multiprocessing.Pool(processes=num_processes) as pool:
                for _ in pool.imap_unordered(game_runner_wrapper, game_tasks):
                    pbar.update(1)
    else:
        logger.info("Running games sequentially.")
        for task in tqdm(game_tasks, desc="Processing Games"):
            game_runner_wrapper(task)

