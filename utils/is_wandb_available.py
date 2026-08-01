
def is_wandb_available():
    if importlib.util.find_spec("wandb") is not None:
        import wandb

        # wandb might still be detected by find_spec after an uninstall (leftover files or metadata), but not actually
        # import correctly. To confirm it's fully installed and usable, we check for a key attribute like "run".
        return hasattr(wandb, "run")
    else:
        return False

