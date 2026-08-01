
def _build_scim_metadata(
    given_name: Optional[str], family_name: Optional[str], active: Optional[bool] = None
) -> Dict[str, Any]:
    """Build metadata dictionary with SCIM data."""
    metadata: Dict[str, Any] = {
        "scim_metadata": LiteLLM_UserScimMetadata(
            givenName=given_name,
            familyName=family_name,
        ).model_dump()
    }

    if active is not None:
        metadata["scim_active"] = active

    return metadata

