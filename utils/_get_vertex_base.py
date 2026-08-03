from typing import Any

def _get_vertex_base() -> Any:
    """Lazily return the shared VertexBase instance to avoid a module-load-time cyclic import."""
    global _GCS_METADATA_VERTEX_BASE
    if _GCS_METADATA_VERTEX_BASE is None:
        from ..vertex_llm_base import VertexBase

        _GCS_METADATA_VERTEX_BASE = VertexBase()
    return _GCS_METADATA_VERTEX_BASE

