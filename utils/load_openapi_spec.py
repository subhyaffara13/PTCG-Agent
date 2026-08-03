from typing import Any, Dict

def load_openapi_spec(filepath: str) -> Dict[str, Any]:
    """
    Sync wrapper. For URL specs, use the shared/custom MCP httpx client.
    """
    try:
        # If we're already inside an event loop, prefer the async function.
        asyncio.get_running_loop()
        raise RuntimeError(
            "load_openapi_spec() was called from within a running event loop. "
            "Use 'await load_openapi_spec_async(...)' instead."
        )
    except RuntimeError as e:
        # "no running event loop" is fine; other RuntimeErrors we re-raise
        if "no running event loop" not in str(e).lower():
            raise
    return asyncio.run(load_openapi_spec_async(filepath))

