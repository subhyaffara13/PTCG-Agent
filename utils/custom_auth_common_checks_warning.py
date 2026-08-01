
def custom_auth_common_checks_warning(
    *,
    custom_auth_configured: bool,
    run_common_checks: bool,
) -> str | None:
    if not custom_auth_configured or run_common_checks:
        return None
    return (
        "custom_auth is configured but 'custom_auth_run_common_checks' is not set. "
        "Problem: budgets, model-access allowlists, and per-model rate limits configured "
        "on your DB team/project records will NOT be enforced for custom-auth requests "
        "(rate limits set directly on the returned UserAPIKeyAuth still apply). "
        "Fix: set 'general_settings.custom_auth_run_common_checks: true'. "
        "Docs: https://docs.litellm.ai/docs/proxy/custom_auth"
    )

