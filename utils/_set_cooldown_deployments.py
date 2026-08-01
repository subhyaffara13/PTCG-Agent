
def _set_cooldown_deployments(
    litellm_router_instance: LitellmRouter,
    original_exception: Any,
    exception_status: Union[str, int],
    deployment: Optional[str] = None,
    time_to_cooldown: Optional[float] = None,
) -> bool:
    """
    Add a model to the list of models being cooled down for that minute, if it exceeds the allowed fails / minute

    or

    the exception is not one that should be immediately retried (e.g. 401)

    Returns:
    - True if the deployment should be put in cooldown
    - False if the deployment should not be put in cooldown
    """
    verbose_router_logger.debug("checks 'should_run_cooldown_logic'")

    if (
        _should_run_cooldown_logic(
            litellm_router_instance=litellm_router_instance,
            deployment=deployment,
            exception_status=exception_status,
            original_exception=original_exception,
            time_to_cooldown=time_to_cooldown,
        )
        is False
        or deployment is None
    ):
        verbose_router_logger.debug("should_run_cooldown_logic returned False")
        return False

    exception_status_int = cast_exception_status_to_int(exception_status)
    verbose_router_logger.debug(f"Attempting to add {deployment} to cooldown list")

    if _should_cooldown_deployment(
        litellm_router_instance=litellm_router_instance,
        deployment=deployment,
        exception_status=exception_status,
        original_exception=original_exception,
    ):
        litellm_router_instance.cooldown_cache.add_deployment_to_cooldown(
            model_id=deployment,
            original_exception=original_exception,
            exception_status=exception_status_int,
            cooldown_time=time_to_cooldown,
        )

        # Trigger cooldown callback handler
        asyncio.create_task(
            router_cooldown_event_callback(
                litellm_router_instance=litellm_router_instance,
                deployment_id=deployment,
                exception_status=exception_status,
                cooldown_time=time_to_cooldown,
            )
        )
        return True
    return False

