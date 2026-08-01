
def get_training_scripts(enable_distributed: bool) -> list:
    if enable_distributed:
        logger.info("Distributed training mode ENABLED.")
        return [
            "distributed/master_server/masterserver.py",
            "distributed/status_server.py",
            "scratch/run_ppo_trainer_loop.py",
            "scratch/run_deck_optimizer_loop.py",
            "scratch/run_bug_hunter.py",
        ]
    logger.info("Local training mode ENABLED.")
    return [
        "scratch/run_deck_optimizer_loop.py",
        "scratch/run_ppo_trainer_loop.py",
        "scratch/run_training_batches.py",
        "scratch/run_bug_hunter.py",
    ]

