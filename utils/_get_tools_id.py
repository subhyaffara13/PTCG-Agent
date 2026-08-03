from typing import Any

def _get_tools_id(node: Any) -> int | None:
    """Return the toolsId for a graph node, or None if unavailable."""
    global _tools_id_available
    if _tools_id_available is None:
        try:
            tools_id = _check_cuda_bindings(
                _cuda_runtime.cudaGraphNodeGetToolsId(  # pyrefly: ignore[missing-attribute]
                    node
                )
            )
        except Exception:
            _tools_id_available = False
            logger.info(
                "cudaGraphNodeGetToolsId not available; "
                "CUDA graph kernel annotations will be disabled"
            )
            return None
        _tools_id_available = True
        return tools_id
    return _check_cuda_bindings(
        _cuda_runtime.cudaGraphNodeGetToolsId(  # pyrefly: ignore[missing-attribute]
            node
        )
    )

