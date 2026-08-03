from typing import Any, Optional

def should_use_emulated_file_search(
    tools: Optional[Iterable[ToolParam]],
    provider_config: Any,  # BaseResponsesAPIConfig
) -> bool:
    """Return True when there is a file_search tool and the provider can't handle it natively."""
    if not tools:
        return False
    has_fs = any(isinstance(t, dict) and t.get("type") == "file_search" for t in tools)
    if not has_fs:
        return False
    return provider_config is None or not provider_config.supports_native_file_search()

