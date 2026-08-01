
def pip_self_version_check_emit(upgrade_prompt: UpgradePrompt | None) -> None:
    """Emit the upgrade prompt captured by :func:`pip_self_version_check_fetch`."""
    if upgrade_prompt is not None:
        logger.warning("%s", upgrade_prompt, extra={"rich": True})

