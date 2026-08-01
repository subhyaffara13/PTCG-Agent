
def _stabilize_multi_method_route_ids(routes) -> None:
    """FastAPI derives route IDs from a set of methods; make snapshots stable."""

    for route in routes:
        methods = sorted(getattr(route, "methods", None) or [])
        if len(methods) <= 1 or not getattr(route, "path_format", None):
            continue

        operation_id = f"{route.name}{route.path_format}"
        operation_id = re.sub(r"\W", "_", operation_id)
        route.unique_id = f"{operation_id}_{methods[0].lower()}"

