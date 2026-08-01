
def load_env_modules():
    """Loads environment variables from repo root."""
    try:
        from kaggle_environments import PROJECT_ROOT
        env_path = os.path.join(PROJECT_ROOT, os.pardir, ".env")
        if os.path.exists(env_path):
            logger.info(f"Loading .env from: {env_path}")
            load_dotenv(env_path)
        else:
            logger.info(f".env not found at {env_path}, relying on system vars.")
    except ImportError:
        logger.warning("Could not import kaggle_environments.PROJECT_ROOT")

