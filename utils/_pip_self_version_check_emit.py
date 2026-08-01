
def _pip_self_version_check_emit(upgrade_prompt: UpgradePrompt | None) -> None:
    from pip._internal.self_outdated_check import pip_self_version_check_emit

    pip_self_version_check_emit(upgrade_prompt)

