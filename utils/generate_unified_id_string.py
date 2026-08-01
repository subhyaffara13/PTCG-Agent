
def generate_unified_id_string(
    resource_type: str,
    unified_uuid: str,
    target_model_names: List[str],
    provider_resource_id: str,
    model_id: str,
    additional_fields: Optional[dict] = None,
) -> str:
    """
    Generate a unified ID string (before base64 encoding).

    Args:
        resource_type: Type of resource (e.g., "vector_store", "file")
        unified_uuid: UUID for this unified resource
        target_model_names: List of target model names
        provider_resource_id: Resource ID from the provider
        model_id: Model ID from the router
        additional_fields: Additional fields to include in the ID

    Returns:
        Unified ID string (not yet base64 encoded)

    Example:
        generate_unified_id_string(
            resource_type="vector_store",
            unified_uuid="abc-123",
            target_model_names=["gpt-4", "gemini"],
            provider_resource_id="vs_xyz",
            model_id="model-id-123",
        )
        returns: "litellm_proxy:vector_store;unified_id,abc-123;target_model_names,gpt-4,gemini;resource_id,vs_xyz;model_id,model-id-123"
    """
    # Build the unified ID string
    parts = [
        f"litellm_proxy:{resource_type}",
        f"unified_id,{unified_uuid}",
        f"target_model_names,{','.join(target_model_names)}",
        f"resource_id,{provider_resource_id}",
        f"model_id,{model_id}",
    ]

    # Add additional fields if provided
    if additional_fields:
        for key, value in additional_fields.items():
            parts.append(f"{key},{value}")

    return ";".join(parts)

