from typing import Optional

def _object_permission_allows_vector_store(
    object_permission: Optional[LiteLLM_ObjectPermissionTable],
    vector_store_id: str,
) -> bool:
    """Returns True if an object permission explicitly allowlists the vector store."""
    if object_permission is None:
        return False
    allowed = object_permission.vector_stores
    if not allowed:
        return False
    return vector_store_id in allowed

