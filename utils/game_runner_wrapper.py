
def game_runner_wrapper(args):
    """Wrapper to unpack arguments for the multiprocessing pool."""
    game_dir, game_config, use_random_agents, debug, _, _ = args
    run_single_game_with_retry(game_dir, game_config, use_random_agents, debug)


def game_runner_wrapper(args):
    """Wrapper to unpack arguments for the multiprocessing pool."""
    game_dir, game_config, use_random_agents, debug, _, _ = args
    run_single_game_with_retry(game_dir, game_config, use_random_agents, debug)


def game_runner_wrapper(args):
    """Wrapper to unpack arguments for the multiprocessing pool."""
    game_dir, game_config, use_random_agents, debug = args
    # This function will be responsible for running a single game.
    # We can use a simplified version of the logic in run_block.py's wrapper.
    # For now, we'll just print the intention.
    # In the next step, we'll implement the actual game running logic.
    # print(f"Running game in: {game_dir}")
    try:
        run_single_game_with_retry(game_dir, game_config, use_random_agents, debug)
    except Exception as e:
        logger.error(f"Game in {game_dir} failed after retries with error: {e}")
        # Optionally, log the full traceback
        logger.debug("Traceback:", exc_info=True)


def game_runner_wrapper(args):
    """Wrapper to unpack arguments for the multiprocessing pool."""
    game_dir, game_config, use_random_agents, debug = args
    run_single_game_with_retry(game_dir, game_config, use_random_agents, debug)

