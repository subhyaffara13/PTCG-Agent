
def _should_route_jwt_to_oauth2_override(token: str, jwt_handler: JWTHandler) -> bool:
    routing_overrides = jwt_handler.litellm_jwtauth.routing_overrides
    if not routing_overrides:
        return False

    token_claims = jwt_handler.get_unverified_claims(token=token)
    if token_claims is None:
        return False

    for override in routing_overrides:
        if override.path == "oauth2" and _matches_routing_override(
            token_claims=token_claims, override=override
        ):
            verbose_proxy_logger.debug(
                "JWT routing override matched. Routing token to OAuth2 introspection."
            )
            return True

    return False

