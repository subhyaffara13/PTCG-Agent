
def get_budget_alert_type(
    type: Literal[
        "token_budget",
        "user_budget",
        "soft_budget",
        "max_budget_alert",
        "team_budget",
        "organization_budget",
        "proxy_budget",
        "projected_limit_exceeded",
        "project_budget",
    ],
) -> BaseBudgetAlertType:
    """Factory function to get the appropriate budget alert type class"""

    alert_types = {
        "proxy_budget": ProxyBudgetAlert(),
        "soft_budget": SoftBudgetAlert(),
        "user_budget": UserBudgetAlert(),
        "max_budget_alert": TokenBudgetAlert(),
        "team_budget": TeamBudgetAlert(),
        "organization_budget": OrganizationBudgetAlert(),
        "token_budget": TokenBudgetAlert(),
        "projected_limit_exceeded": ProjectedLimitExceededAlert(),
        "project_budget": ProjectBudgetAlert(),
    }

    if type in alert_types:
        return alert_types[type]
    else:
        return ProxyBudgetAlert()

