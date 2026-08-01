
def _matches_routing_override(
    token_claims: dict, override: "JWTRoutingOverride"
) -> bool:
    return (
        _routing_selector_matches_claim(override.iss, token_claims.get("iss"))
        and _routing_selector_matches_claim(
            override.client_id, token_claims.get("client_id")
        )
        and _routing_selector_matches_claim(
            override.scope,
            token_claims.get("scope"),
            split_space_delimited=True,
        )
        and _routing_selector_matches_claim(override.aud, token_claims.get("aud"))
    )

