
def handle_push_failure():
    import logging
    logger = logging.getLogger("orchestrator_master_git")
    try:
        _run_git(["git", "pull", "--rebase"], check=True, capture_output=True, text=True)
        _run_git(["git", "push"], check=True, capture_output=True, text=True)
        logger.info("Factory updates rebased and pushed successfully.")
    except Exception as rebase_err:
        logger.error(f"Git rebase/push recovery failed: {rebase_err}")
        raise

