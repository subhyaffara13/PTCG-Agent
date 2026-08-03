from typing import Any, Optional

def _raise_if_model_fully_blocked(
    llm_router: LitellmRouter, model_name: Any, team_id: Optional[str]
) -> None:
    if not isinstance(model_name, str) or not model_name:
        return
    if not isinstance(llm_router, litellm.Router):
        return
    deployments = (
        llm_router.get_model_list(model_name=model_name, team_id=team_id) or []
    )
    if llm_router._are_all_deployments_blocked(deployments):
        raise litellm.PermissionDeniedError(
            message="Model is blocked",
            model=model_name,
            llm_provider="",
            response=httpx.Response(
                status_code=403,
                request=httpx.Request(
                    method="POST", url="https://github.com/BerriAI/litellm"
                ),
            ),
        )

