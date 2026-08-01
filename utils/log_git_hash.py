
def log_git_hash():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,  # Don't raise exception on non-zero exit code
        )
        if result.returncode == 0:
            git_hash = result.stdout.strip()
            logger.info(f"Running from git commit: {git_hash}")
        else:
            logger.info("Not a git repository or git command failed.")
    except FileNotFoundError:
        logger.info("Git command not found.")

