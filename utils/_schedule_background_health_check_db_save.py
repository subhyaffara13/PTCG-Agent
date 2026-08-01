
def _schedule_background_health_check_db_save(
    prisma_client,
    shared_health_manager,
    model_list: list,
    healthy_endpoints: list,
    unhealthy_endpoints: list,
):
    """Fire-and-forget: persist health check results to DB if prisma is available."""
    if prisma_client is None:
        return
    import time as time_module

    from litellm.proxy.health_endpoints._health_endpoints import (
        _save_background_health_checks_to_db,
    )

    checked_by = (
        shared_health_manager.pod_id
        if shared_health_manager is not None
        else "background_health_check"
    )
    start_time = time_module.time()
    asyncio.create_task(
        _save_background_health_checks_to_db(
            prisma_client,
            model_list,
            healthy_endpoints,
            unhealthy_endpoints,
            start_time,
            checked_by=checked_by,
        )
    )

