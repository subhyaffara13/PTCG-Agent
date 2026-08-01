
def warn_once_if_custom_auth_skips_common_checks(
    *,
    custom_auth_configured: bool,
    run_common_checks: bool,
    logger: Logger = verbose_proxy_logger,
) -> None:
    global _custom_auth_common_checks_warning_emitted
    if _custom_auth_common_checks_warning_emitted:
        return
    message = custom_auth_common_checks_warning(
        custom_auth_configured=custom_auth_configured,
        run_common_checks=run_common_checks,
    )
    if message is None:
        return
    logger.warning(message)
    _custom_auth_common_checks_warning_emitted = True

