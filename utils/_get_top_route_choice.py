
def _get_top_route_choice(result: Any) -> Any:
    """Extract the top RouteChoice from SemanticRouter result.

    SemanticRouter.__call__ can return RouteChoice or List[RouteChoice].
    """
    if result is None:
        return None
    if isinstance(result, list):
        return result[0] if result else None
    return result

