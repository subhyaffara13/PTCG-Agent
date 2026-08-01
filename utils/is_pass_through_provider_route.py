
def is_pass_through_provider_route(route: str) -> bool:
    PROVIDER_SPECIFIC_PASS_THROUGH_ROUTES = [
        "vertex-ai",
    ]

    # check if any of the prefixes are in the route
    for prefix in PROVIDER_SPECIFIC_PASS_THROUGH_ROUTES:
        if prefix in route:
            return True

    return False

