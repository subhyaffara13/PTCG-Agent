from typing import List, Optional

def _can_object_call_vector_stores(
    object_type: Literal["key", "team", "org"],
    vector_store_ids_to_run: List[str],
    object_permissions: Optional[LiteLLM_ObjectPermissionTable],
):
    """
    Raises ProxyException if the object (key, team, org) cannot access the specific vector store.
    """
    if object_permissions is None:
        return True

    if object_permissions.vector_stores is None:
        return True

    # If length is 0, then the object has access to all vector stores.
    if len(object_permissions.vector_stores) == 0:
        return True

    for vector_store_id in vector_store_ids_to_run:
        if vector_store_id not in object_permissions.vector_stores:
            raise ProxyException(
                message=f"User not allowed to access vector store. Tried to access {vector_store_id}. Only allowed to access {object_permissions.vector_stores}",
                type=ProxyErrorTypes.get_vector_store_access_error_type_for_object(
                    object_type
                ),
                param="vector_store",
                code=status.HTTP_401_UNAUTHORIZED,
            )

    return True

