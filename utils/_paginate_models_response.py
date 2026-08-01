
def _paginate_models_response(
    all_models: List[Dict[str, Any]],
    page: int,
    size: int,
    total_count: Optional[int],
    search: Optional[str],
) -> Dict[str, Any]:
    """
    Paginate models and return response dictionary.

    Args:
        all_models: List of all models
        page: Current page number
        size: Page size
        total_count: Total count (if None, uses len(all_models))
        search: Search term (for logging)

    Returns:
        Paginated response dictionary
    """
    if total_count is None:
        total_count = len(all_models)

    skip = (page - 1) * size
    total_pages = -(-total_count // size) if total_count > 0 else 0
    paginated_models = all_models[skip : skip + size]

    verbose_proxy_logger.debug(
        f"Pagination: skip={skip}, take={size}, total_count={total_count}, total_pages={total_pages}, search={search}"
    )

    return {
        "data": paginated_models,
        "total_count": total_count,
        "current_page": page,
        "total_pages": total_pages,
        "size": size,
    }

