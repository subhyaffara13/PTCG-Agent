
def _run_single_game(config: GameConfig, log_dir: str) -> GameResult:
    """
    Worker function that runs a single game in a separate process.
    """
    try:
        from factory.game_runner import GameRunner
        runner = GameRunner(log_dir=log_dir)
        result = runner.run_iteration(
            iteration_id=config.iteration_id,
            version_n1=config.version_a,
            version_n2=config.version_b,
            deck_base=config.deck_a,
            deck_new=config.deck_b,
            reasoning_base=config.reasoning_a,
            reasoning_new=config.reasoning_b,
        )
        return GameResult(config=config, result=result, success=True)
    except Exception as e:
        logger.error(f"Game {config.label or config.iteration_id} failed: {e}", exc_info=True)
        return GameResult(config=config, result=None, success=False, error=str(e))

