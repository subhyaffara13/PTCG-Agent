from typing import Union

def cast_exception_status_to_int(exception_status: Union[str, int]) -> int:
    if isinstance(exception_status, str):
        try:
            exception_status = int(exception_status)
        except Exception:
            verbose_router_logger.debug(
                f"Unable to cast exception status to int {exception_status}. Defaulting to status=500."
            )
            exception_status = 500
    return exception_status

