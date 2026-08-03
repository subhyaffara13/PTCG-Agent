from typing import Dict, Optional

def _update_request_data_with_managed_file_id(
    data: Dict,
    file_id: str,
    request: Request,
    llm_router: Optional["Router"] = None,
) -> tuple[Dict, Optional[str]]:
    """
    Update request data with model routing information from managed file ID.

    This function handles two types of file IDs:
    1. Simple encoded file IDs (format: litellm:{file_id};model,{model})
    2. Unified managed file IDs (format: litellm_proxy:{mime};unified_id,{uuid};...;llm_output_file_id,{file_id};...)

    For unified managed file IDs, it:
    - Decodes the unified ID to extract the actual provider file ID (llm_output_file_id)
    - Extracts the model routing information (target_model_names)
    - Updates data with credentials for the correct deployment

    Args:
        data: Request data to update
        file_id: File ID (can be managed/encoded or regular)
        request: FastAPI request object
        llm_router: LiteLLM router for credential lookup (required for managed files)

    Returns:
        Tuple of (updated request data, original_managed_file_id)
        - original_managed_file_id is the original file_id if it was managed/encoded, None otherwise
    """
    import re

    from litellm import verbose_logger
    from litellm.llms.base_llm.managed_resources.utils import (
        is_base64_encoded_unified_id,
        parse_unified_id,
    )

    # First, check if this is a unified managed file ID (base64 encoded)
    decoded_id = is_base64_encoded_unified_id(file_id)

    if decoded_id:
        # This is a unified managed file ID
        verbose_logger.debug(f"Processing unified managed file ID: {file_id}")

        # Parse the unified ID to extract components
        parsed_id = parse_unified_id(file_id)

        if parsed_id:
            target_model_names = parsed_id.get("target_model_names", [])

            # Extract the actual provider file ID from llm_output_file_id field
            # Format: litellm_proxy:...;llm_output_file_id,{actual_file_id};...
            llm_output_file_id = None
            try:
                match = re.search(r"llm_output_file_id,([^;]+)", decoded_id)
                if match:
                    llm_output_file_id = match.group(1).strip()
            except Exception:
                pass

            verbose_logger.debug(
                f"Decoded unified file ID - target_model_names: {target_model_names}, llm_output_file_id: {llm_output_file_id}"
            )

            # Set the model for routing
            if target_model_names and len(target_model_names) > 0:
                routing_model = target_model_names[0]
                data["model"] = routing_model

                # Get credentials for the model
                if llm_router:
                    credentials = llm_router.get_deployment_credentials_with_provider(
                        model_id=routing_model
                    )
                    if credentials:
                        prepare_data_with_credentials(
                            data=data,
                            credentials=credentials,
                            file_id=llm_output_file_id,  # Use the actual provider file ID
                        )
                        verbose_logger.info(
                            f"Routing vector store file operation to model: {routing_model}, file_id: {file_id} -> {llm_output_file_id}"
                        )
                        return data, file_id  # Return original managed file ID

            # If we extracted the provider file ID but no routing, still use it
            if llm_output_file_id:
                data["file_id"] = llm_output_file_id
                verbose_logger.debug(
                    f"Replaced unified file ID with provider file ID: {llm_output_file_id}"
                )
                return data, file_id  # Return original managed file ID

        return data, file_id if decoded_id else None

    # Fall back to simple encoded file ID handling (format: litellm:{file_id};model,{model})
    (
        should_route,
        model_used,
        original_file_id,
        credentials,
    ) = handle_model_based_routing(
        file_id=file_id,
        request=request,
        llm_router=llm_router,
        data=data,
        check_file_id_encoding=True,
    )

    if should_route:
        # Use model-based routing with credentials from config
        prepare_data_with_credentials(
            data=data,
            credentials=credentials,  # type: ignore
            file_id=original_file_id,  # Use decoded file ID if from encoded ID
        )

        verbose_logger.debug(
            f"Routing vector store file operation using model: {model_used}"
            + (
                f", file_id: {file_id} -> {original_file_id}"
                if original_file_id
                else ""
            )
        )
        return data, file_id  # Return original file ID for response replacement

    return data, None

