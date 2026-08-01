
def _is_input_only_route(route: str) -> bool:
    return any(
        route_part in route
        for route_part in (
            "embeddings",
            "rerank",
            "moderations",
        )
    )

