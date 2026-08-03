import logging

logger = logging.getLogger("orchestration_agent")

def get_training_scripts(enable_distributed: bool) -> list:
    if enable_distributed:
        logger.info("Distributed training mode ENABLED.")
        return [
            "distributed/master_server/masterserver.py",
            "distributed/status_server.py",
            "run_guided_iterations.py",
            "run_factory.py",
        ]
    logger.info("Local training mode ENABLED.")
    return [
        "run_guided_iterations.py",
        "run_factory.py",
    ]
