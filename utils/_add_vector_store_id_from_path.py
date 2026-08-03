import re

def _add_vector_store_id_from_path(request_data: dict, request: Request) -> None:
    """
    Parse the request path to find /vector_stores/{vector_store_id}/... segments.

    When found, ensure both vector_store_id and vector_store_ids are populated.

    Args:
        request_data: The request data dictionary to populate
        request: The FastAPI Request object
    """
    # Inline import — auth_utils participates in a proxy import cycle.
    from litellm.proxy.auth.auth_utils import get_request_route  # noqa: PLC0415

    path = get_request_route(request)
    vector_store_match = re.search(r"/vector_stores/([^/]+)/", path)
    if vector_store_match:
        vector_store_id = vector_store_match.group(1)
        verbose_proxy_logger.debug(
            f"populate_request_with_path_params: Extracted vector_store_id={vector_store_id} from path={path}"
        )
        request_data.setdefault("vector_store_id", vector_store_id)
        existing_ids = request_data.get("vector_store_ids")
        if isinstance(existing_ids, list):
            if vector_store_id not in existing_ids:
                existing_ids.append(vector_store_id)
        else:
            request_data["vector_store_ids"] = [vector_store_id]
        verbose_proxy_logger.debug(
            f"populate_request_with_path_params: Updated request_data with vector_store_ids={request_data.get('vector_store_ids')}"
        )
    else:
        verbose_proxy_logger.debug(
            f"populate_request_with_path_params: No vector_store_id present in path={path}"
        )

