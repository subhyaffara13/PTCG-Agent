from typing import Any, Dict

def extract_text_from_a2a_response(response_dict: Dict[str, Any]) -> str:
    return A2ARequestUtils.extract_text_from_response(response_dict)


def extract_text_from_a2a_response(
    response_dict: Dict[str, Any], max_depth: int = 10
) -> str:
    """
    Extract text content from A2A response result.

    Args:
        response_dict: A2A response dict with 'result' containing message
        max_depth: Maximum recursion depth to prevent infinite loops

    Returns:
        Text from response message parts
    """
    result = response_dict.get("result", {})
    if not isinstance(result, dict):
        return ""

    # A2A response can have different formats:
    # 1. Direct message: {"result": {"kind": "message", "parts": [...]}}
    # 2. Nested message: {"result": {"message": {"parts": [...]}}}
    # 3. Task with artifacts: {"result": {"kind": "task", "artifacts": [{"parts": [...]}]}}
    # 4. Task with status message: {"result": {"kind": "task", "status": {"message": {"parts": [...]}}}}
    # 5. Streaming artifact-update: {"result": {"kind": "artifact-update", "artifact": {"parts": [...]}}}

    # Check if result itself has parts (direct message)
    if "parts" in result:
        return extract_text_from_a2a_message(result, depth=0, max_depth=max_depth)

    # Check for nested message
    message = result.get("message")
    if message:
        return extract_text_from_a2a_message(message, depth=0, max_depth=max_depth)

    # Check for streaming artifact-update (singular artifact)
    artifact = result.get("artifact")
    if artifact and isinstance(artifact, dict):
        return extract_text_from_a2a_message(artifact, depth=0, max_depth=max_depth)

    # Check for task status message (common in Gemini A2A agents)
    status = result.get("status", {})
    if isinstance(status, dict):
        status_message = status.get("message")
        if status_message:
            return extract_text_from_a2a_message(
                status_message, depth=0, max_depth=max_depth
            )

    # Handle task result with artifacts (plural, array)
    artifacts = result.get("artifacts", [])
    if artifacts and len(artifacts) > 0:
        first_artifact = artifacts[0]
        return extract_text_from_a2a_message(
            first_artifact, depth=0, max_depth=max_depth
        )

    return ""

