from typing import Dict, Optional

def validate_model_max_budget(model_max_budget: Optional[Dict]) -> None:
    """
    Validate the model_max_budget is GenericBudgetConfigType + enforce user has an enterprise license

    Raises:
        Exception: If model_max_budget is not a valid GenericBudgetConfigType
    """
    try:
        if model_max_budget is None:
            return
        if len(model_max_budget) == 0:
            return
        if model_max_budget is not None:
            from litellm.proxy.proxy_server import CommonProxyErrors, premium_user

            if premium_user is not True:
                raise ValueError(
                    f"You must have an enterprise license to set model_max_budget. {CommonProxyErrors.not_premium_user.value}"
                )
            for _model, _budget_info in model_max_budget.items():
                assert isinstance(_model, str)

                # Normalize to dict (Pydantic may already parse nested values as BudgetConfig)
                _info = (
                    _budget_info.model_dump()
                    if hasattr(_budget_info, "model_dump")
                    else dict(_budget_info)
                )
                # /CRUD endpoints can pass budget_limit as a string, so we need to convert it to a float
                if "budget_limit" in _info:
                    _info["budget_limit"] = float(_info["budget_limit"])
                BudgetConfig(**_info)
    except Exception as e:
        raise ValueError(
            f"Invalid model_max_budget: {str(e)}. Example of valid model_max_budget: https://docs.litellm.ai/docs/proxy/users"
        )

