
def set_result(fut: "asyncio.Future[_T]", result: _T) -> None:
    if not fut.done():
        fut.set_result(result)

