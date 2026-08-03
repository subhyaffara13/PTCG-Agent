import time

def run_single_iteration(iteration, enable_distributed, inference_server):
    from factory.log_pruner import prune_logs
    from factory.teams.development_team import DevelopmentTeam
    from .run_hourly_checks import run_hourly_checks
    logger.info("--- [Train Phase] Starting training processes ---")
    scripts = get_training_scripts(enable_distributed=enable_distributed)
    processes = launch_processes(scripts)
    try:
        for _ in range(10):
            monitor_and_restart(processes, scripts); time.sleep(60)
    except KeyboardInterrupt: raise
    finally:
        try: cleanup(processes); time.sleep(2)
        except KeyboardInterrupt: pass
    prune_logs(max_files=1000)
    try: DevelopmentTeam().run_development(iteration)
    except Exception as e: logger.error(f"Development Team cycle failed: {e}", exc_info=True)
    run_hourly_checks(iteration); run_analytics_check(iteration)
    try:
        from factory.league_manager import LeagueManager
        from factory.tensorboard_logger import TBLogger
        lm = LeagueManager(); tb = TBLogger.get()
        for agent_name, rating in lm.ratings.items(): tb.log_scalar(f"league_elo/{agent_name}", rating, iteration)
        tb.flush()
    except Exception as e: logger.debug(f"Failed to log ELO: {e}")
    if enable_distributed:
        try:
            from factory.orchestrator_master_git import auto_commit_and_push_if_changed
            auto_commit_and_push_if_changed()
        except Exception as e: logger.error(f"Git auto-push failed: {e}")

