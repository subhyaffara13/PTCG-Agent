from typing import Dict, Optional

def _update_request_data_with_litellm_managed_vector_store_registry(
    data: Dict,
    vector_store_id: str,
    llm_router: Optional["Router"] = None,
    managed_vector_store: Optional[LiteLLM_ManagedVectorStore] = None,
    should_lookup_registry: bool = True,
) -> Dict:
    """
    Update request data with model routing information from managed vector store.

    This function handles two types of vector stores:
    1. Legacy vector stores from registry (non-managed)
    2. Managed vector stores with unified IDs (requires decoding)

    For managed vector stores, this function:
    - Decodes the unified vector store ID
    - Extracts the model_id and provider resource ID
    - Sets data["model"] so the router can use the correct deployment credentials
    - Replaces the unified ID with the provider-specific ID

    Args:
        data: Request data to update
        vector_store_id: Vector store ID (can be unified or legacy)
        llm_router: LiteLLM router for credential lookup (required for managed vector stores)

    Returns:
        Updated request data with model routing information
    """
    from litellm import verbose_logger
    from litellm.llms.base_llm.managed_resources.utils import (
        is_base64_encoded_unified_id,
        parse_unified_id,
    )

    # Check if this is a managed vector store ID (base64 encoded unified ID)
    decoded_id = is_base64_encoded_unified_id(vector_store_id)

    if decoded_id:
        # This is a managed vector store - decode and extract routing information
        verbose_logger.debug(f"Processing managed vector store ID: {vector_store_id}")

        parsed_id = parse_unified_id(vector_store_id)

        if parsed_id:
            model_id = parsed_id.get("model_id")
            provider_resource_id = parsed_id.get("provider_resource_id")
            target_model_names = parsed_id.get("target_model_names", [])

            verbose_logger.debug(
                f"Decoded vector store - model_id: {model_id}, provider_resource_id: {provider_resource_id}, target_model_names: {target_model_names}"
            )

            # Set the model for routing - this tells the router which deployment to use
            # The router will automatically get the credentials from the deployment
            routing_model = None
            if model_id:
                routing_model = model_id
            elif target_model_names and len(target_model_names) > 0:
                routing_model = target_model_names[0]

            if routing_model:
                data["model"] = routing_model
                verbose_logger.info(
                    f"Routing vector store files operation to model: {routing_model}"
                )

            # Replace unified vector store ID with provider resource ID
            if provider_resource_id:
                data["vector_store_id"] = provider_resource_id
                verbose_logger.debug(
                    f"Replaced unified vector store ID with provider resource ID: {provider_resource_id}"
                )

        return data

    # Legacy path: Check vector store registry for non-managed vector stores.
    vector_store_to_run = managed_vector_store
    if (
        vector_store_to_run is None
        and should_lookup_registry
        and litellm.vector_store_registry is not None
    ):
        vector_store_to_run = litellm.vector_store_registry.get_litellm_managed_vector_store_from_registry(
            vector_store_id=vector_store_id
        )

    if vector_store_to_run is not None:
        if "custom_llm_provider" in vector_store_to_run:
            data["custom_llm_provider"] = vector_store_to_run.get("custom_llm_provider")
        if "litellm_credential_name" in vector_store_to_run:
            data["litellm_credential_name"] = vector_store_to_run.get(
                "litellm_credential_name"
            )
        if "litellm_params" in vector_store_to_run:
            litellm_params = vector_store_to_run.get("litellm_params", {}) or {}
            data.update(litellm_params)

    return data

