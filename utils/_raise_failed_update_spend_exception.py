import time

def _raise_failed_update_spend_exception(
    e: Exception, start_time: float, proxy_logging_obj: ProxyLogging
):
    """
    Raise an exception for failed update spend logs

    - Calls proxy_logging_obj.failure_handler to log the error
    - Ensures error messages says "Non-Blocking"
    """
    import traceback

    error_msg = (
        f"[Non-Blocking]LiteLLM Prisma Client Exception - update spend logs: {str(e)}"
    )
    error_traceback = error_msg + "\n" + traceback.format_exc()
    end_time = time.time()
    _duration = end_time - start_time
    asyncio.create_task(
        proxy_logging_obj.failure_handler(
            original_exception=e,
            duration=_duration,
            call_type="update_spend",
            traceback_str=error_traceback,
        )
    )
    raise e

