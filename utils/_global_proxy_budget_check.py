
def _global_proxy_budget_check(
    global_proxy_spend: Optional[float], skip_budget_checks: bool, route: str
) -> None:
    if (
        litellm.max_budget > 0
        and not skip_budget_checks
        and global_proxy_spend is not None
        and RouteChecks.is_llm_api_route(route=route)
        and route != "/v1/models"
        and route != "/models"
    ):
        if (
            math.isfinite(litellm.max_budget)
            and global_proxy_spend > litellm.max_budget
        ):
            raise litellm.BudgetExceededError(
                current_cost=global_proxy_spend, max_budget=litellm.max_budget
            )

