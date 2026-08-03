from typing import Any, Optional, Union
import math


def _should_run_cooldown_logic(
    litellm_router_instance: LitellmRouter,
    deployment: Optional[str],
    exception_status: Union[str, int],
    original_exception: Any,
    time_to_cooldown: Optional[float] = None,
) -> bool:
    """
    Helper that decides if cooldown logic should be run
    Returns False if cooldown logic should not be run

    Does not run cooldown logic when:
    - router.disable_cooldowns is True
    - deployment is None
    - _is_cooldown_required() returns False
    - deployment is in litellm_router_instance.provider_default_deployment_ids
    - exception_status is not one that should be immediately retried (e.g. 401)
    """
    if (
        deployment is None
        or litellm_router_instance.get_model_group(id=deployment) is None
    ):
        verbose_router_logger.debug(
            "Should Not Run Cooldown Logic: deployment id is none or model group can't be found."
        )
        return False

    #########################################################
    # If time_to_cooldown is 0 or 0.0000000, don't run cooldown logic
    #########################################################
    if time_to_cooldown is not None and math.isclose(
        a=time_to_cooldown, b=0.0, abs_tol=1e-9
    ):
        verbose_router_logger.debug(
            "Should Not Run Cooldown Logic: time_to_cooldown is effectively 0"
        )
        return False

    if litellm_router_instance.disable_cooldowns:
        verbose_router_logger.debug(
            "Should Not Run Cooldown Logic: disable_cooldowns is True"
        )
        return False

    if deployment is None:
        verbose_router_logger.debug("Should Not Run Cooldown Logic: deployment is None")
        return False

    if not _is_cooldown_required(
        litellm_router_instance=litellm_router_instance,
        model_id=deployment,
        exception_status=exception_status,
        exception_str=str(original_exception),
    ):
        verbose_router_logger.debug(
            "Should Not Run Cooldown Logic: _is_cooldown_required returned False"
        )
        return False

    if deployment in litellm_router_instance.provider_default_deployment_ids:
        verbose_router_logger.debug(
            "Should Not Run Cooldown Logic: deployment is in provider_default_deployment_ids"
        )
        return False

    return True

