
def _redis_circuit_breaker_guard(method):  # type: ignore
    """
    Decorator for RedisCache async methods.
    Checks the circuit breaker before each call; records success/failure after.
    Does not apply to ping/disconnect/test_connection (health/teardown must always run).
    """

    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):  # type: ignore
        if self._circuit_breaker.is_open():
            raise Exception(
                f"Redis circuit breaker is open — skipping {method.__name__}"
            )
        try:
            result = await method(self, *args, **kwargs)
            self._circuit_breaker.record_success()
            return result
        except Exception:
            self._circuit_breaker.record_failure()
            raise

    return wrapper

