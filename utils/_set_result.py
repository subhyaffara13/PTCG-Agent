
def _set_result(wait_next: "asyncio.Future[None]") -> None:
    """Set the result of a future if it is not already done."""
    if not wait_next.done():
        wait_next.set_result(None)

