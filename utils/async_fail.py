
def async_fail(nodeid: str) -> None:
    msg = (
        "async def functions are not natively supported.\n"
        "You need to install a suitable plugin for your async framework, for example:\n"
        "  - anyio\n"
        "  - pytest-asyncio\n"
        "  - pytest-tornasync\n"
        "  - pytest-trio\n"
        "  - pytest-twisted"
    )
    fail(msg, pytrace=False)

