
def _extract_model_from_bedrock_endpoint(endpoint: str) -> str:
    """
    Extract model name from Bedrock endpoint path.

    Handles model names with slashes (e.g., aws/anthropic/bedrock-claude-3-5-sonnet-v1)
    by finding the action in the endpoint and extracting everything between "model" and the action.

    Args:
        endpoint: The endpoint path (e.g., "/model/aws/anthropic/model-name/invoke" or "v2/model/model-name/invoke")

    Returns:
        The extracted model name (e.g., "aws/anthropic/model-name" or "model-name")

    Raises:
        ValueError: If model cannot be extracted from endpoint
    """
    try:
        endpoint_parts = endpoint.split("/")

        if "application-inference-profile" in endpoint:
            # Format: model/application-inference-profile/{profile-id}/{action}
            return "/".join(endpoint_parts[1:3])

        # Format: model/{modelId}/{action} or v2/model/{modelId}/{action}
        # Find the index of "model" in the endpoint parts
        model_index = None
        for idx, part in enumerate(endpoint_parts):
            if part == "model":
                model_index = idx
                break

        # If "model" keyword not found, try to extract model from the endpoint
        # by finding the action and taking everything before it
        if model_index is None:
            # Find the index of the action in the endpoint parts
            action_index = None
            for idx, part in enumerate(endpoint_parts):
                if part in BEDROCK_ENDPOINT_ACTIONS:
                    action_index = idx
                    break

            if action_index is not None and action_index > 1:
                # Join all parts before the action (excluding empty strings)
                model_parts = [p for p in endpoint_parts[1:action_index] if p]
                if model_parts:
                    return "/".join(model_parts)

            raise ValueError(
                f"'model' keyword not found and unable to extract model from endpoint. Expected format: /model/{{modelId}}/{{action}}. Got: {endpoint}"
            )

        # Find the index of the action in the endpoint parts
        action_index = None
        for idx, part in enumerate(endpoint_parts):
            if part in BEDROCK_ENDPOINT_ACTIONS:
                action_index = idx
                break

        if action_index is not None and action_index > model_index + 1:
            # Join all parts between "model" and the action (excluding "model" itself)
            return "/".join(endpoint_parts[model_index + 1 : action_index])

        # Fallback to taking everything after "model" if no action found
        model_parts = [p for p in endpoint_parts[model_index + 1 :] if p]
        if model_parts:
            return "/".join(model_parts)

        raise ValueError(
            f"No model ID found after 'model' keyword. Expected format: /model/{{modelId}}/{{action}}. Got: {endpoint}"
        )

    except ValueError:
        # Re-raise ValueError as-is
        raise
    except Exception as e:
        raise ValueError(
            f"Model missing from endpoint. Expected format: /model/{{modelId}}/{{action}}. Got: {endpoint}"
        ) from e

