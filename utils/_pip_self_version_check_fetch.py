
def _pip_self_version_check_fetch(
    session: PipSession, options: Values
) -> UpgradePrompt | None:
    from pip._internal.self_outdated_check import pip_self_version_check_fetch

    return pip_self_version_check_fetch(session, options)

