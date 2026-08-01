
def _raise_budget_unverifiable(counter_key: str) -> None:
    verbose_proxy_logger.warning(
        "fail_closed_budget_enforcement: rejecting request — spend for %s could "
        "not be verified against Redis or the database",
        counter_key,
    )
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail={
            "error": (
                "Budget enforcement unavailable: current spend could not be "
                "verified against Redis or the database, and "
                "fail_closed_budget_enforcement is enabled, so the request was "
                "rejected to avoid exceeding the configured budget. Retry shortly."
            )
        },
    )

