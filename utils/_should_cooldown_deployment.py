
def _should_cooldown_deployment(
    litellm_router_instance: LitellmRouter,
    deployment: str,
    exception_status: Union[str, int],
    original_exception: Any,
) -> bool:
    """
    Helper that decides if a deployment should be put in cooldown

    Returns True if the deployment should be put in cooldown
    Returns False if the deployment should not be put in cooldown


    Deployment is put in cooldown when:
    - v2 logic (Current):
    cooldown if:
        - got a 429 error from LLM API
        - if %fails/%(successes + fails) > ALLOWED_FAILURE_RATE_PER_MINUTE
        - got 401 Auth error, 404 NotFounder - checked by litellm._should_retry()



    - v1 logic (Legacy): if allowed fails or allowed fail policy set, coolsdown if num fails in this minute > allowed fails
    """
    ## BASE CASE - single deployment
    model_group = litellm_router_instance.get_model_group(id=deployment)
    is_single_deployment_model_group = False
    if model_group is not None and len(model_group) == 1:
        is_single_deployment_model_group = True
    if (
        litellm_router_instance.allowed_fails_policy is None
        and _is_allowed_fails_set_on_router(
            litellm_router_instance=litellm_router_instance
        )
        is False
    ):
        num_successes_this_minute = get_deployment_successes_for_current_minute(
            litellm_router_instance=litellm_router_instance, deployment_id=deployment
        )
        num_fails_this_minute = get_deployment_failures_for_current_minute(
            litellm_router_instance=litellm_router_instance, deployment_id=deployment
        )

        total_requests_this_minute = num_successes_this_minute + num_fails_this_minute
        percent_fails = 0.0
        if total_requests_this_minute > 0:
            percent_fails = num_fails_this_minute / (
                num_successes_this_minute + num_fails_this_minute
            )
        verbose_router_logger.debug(
            "percent fails for deployment = %s, percent fails = %s, num successes = %s, num fails = %s",
            deployment,
            percent_fails,
            num_successes_this_minute,
            num_fails_this_minute,
        )

        exception_status_int = cast_exception_status_to_int(exception_status)
        if exception_status_int == 429 and not is_single_deployment_model_group:
            return True
        elif (
            percent_fails == 1.0
            and total_requests_this_minute
            >= SINGLE_DEPLOYMENT_TRAFFIC_FAILURE_THRESHOLD
        ):
            # Cooldown if all requests failed and we have reasonable traffic
            return True
        elif (
            percent_fails > DEFAULT_FAILURE_THRESHOLD_PERCENT
            and total_requests_this_minute >= DEFAULT_FAILURE_THRESHOLD_MINIMUM_REQUESTS
            and not is_single_deployment_model_group  # by default we should avoid cooldowns on single deployment model groups
        ):
            # Only apply error rate cooldown when we have enough requests to make the percentage meaningful
            return True

        elif (
            litellm._should_retry(
                status_code=cast_exception_status_to_int(exception_status)
            )
            is False
        ):
            return True

        return False
    else:
        return should_cooldown_based_on_allowed_fails_policy(
            litellm_router_instance=litellm_router_instance,
            deployment=deployment,
            original_exception=original_exception,
        )

    return False

