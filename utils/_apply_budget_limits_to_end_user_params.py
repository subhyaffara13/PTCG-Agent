from typing import Optional

def _apply_budget_limits_to_end_user_params(
    end_user_params: dict,
    budget_info: LiteLLM_BudgetTable,
    end_user_id: Optional[str],
) -> None:
    """
    Helper function to apply budget limits to end user parameters.

    Args:
        end_user_params: Dictionary to update with budget parameters
        budget_info: Budget table object containing limits
        end_user_id: ID of the end user for logging
    """
    if budget_info.tpm_limit is not None:
        end_user_params["end_user_tpm_limit"] = budget_info.tpm_limit

    if budget_info.rpm_limit is not None:
        end_user_params["end_user_rpm_limit"] = budget_info.rpm_limit

    if budget_info.max_budget is not None:
        end_user_params["end_user_max_budget"] = budget_info.max_budget

    if budget_info.model_max_budget is not None:
        end_user_params["end_user_model_max_budget"] = budget_info.model_max_budget

    verbose_proxy_logger.debug(f"Applied budget limits to end user {end_user_id}")

