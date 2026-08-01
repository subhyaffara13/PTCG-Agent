
def _to_response(mapping) -> JWTKeyMappingResponse:
    """Convert a Prisma mapping object to a safe response (no hashed token)."""
    return JWTKeyMappingResponse(
        id=mapping.id,
        jwt_claim_name=mapping.jwt_claim_name,
        jwt_claim_value=mapping.jwt_claim_value,
        description=mapping.description,
        is_active=mapping.is_active,
        created_at=mapping.created_at,
        updated_at=mapping.updated_at,
        created_by=mapping.created_by,
        updated_by=mapping.updated_by,
    )

