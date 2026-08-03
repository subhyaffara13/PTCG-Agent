from typing import Any

def _get_async_compile() -> Any:
    """Get or create the shared AsyncCompile instance."""
    global _async_compile
    if _async_compile is None:
        from torch._inductor.async_compile import AsyncCompile

        _async_compile = AsyncCompile()
    return _async_compile

