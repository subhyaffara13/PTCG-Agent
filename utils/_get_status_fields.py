from typing import Dict, List, Optional

def _get_status_fields(
    status: StandardLoggingPayloadStatus,
    guardrail_information: Optional[List[dict]],
    error_str: Optional[str],
) -> "StandardLoggingPayloadStatusFields":
    """
    Determine status fields based on request status and guardrail information.

    Args:
        status: Overall request status ("success" or "failure")
        guardrail_information: Guardrail information from metadata
        error_str: Error string if any

    Returns:
        StandardLoggingPayloadStatusFields with llm_api_status and guardrail_status
    """
    # Mapping for legacy guardrail status values to new GuardrailStatus values
    GUARDRAIL_STATUS_MAP: Dict[str, GuardrailStatus] = {
        "success": "success",
        "blocked": "guardrail_intervened",  # legacy
        "guardrail_intervened": "guardrail_intervened",  # direct
        "failure": "guardrail_failed_to_respond",  # legacy
        "guardrail_failed_to_respond": "guardrail_failed_to_respond",  # direct
        "not_run": "not_run",
    }

    # Set LLM API status
    llm_api_status: StandardLoggingPayloadStatus = status

    #########################################################
    # Map - guardrail_information.guardrail_status to guardrail_status
    #########################################################
    guardrail_status: GuardrailStatus = "not_run"
    if guardrail_information and isinstance(guardrail_information, list):
        for information in guardrail_information:
            if isinstance(information, dict):
                raw_status = information.get("guardrail_status", "not_run")
                if raw_status != "not_run":
                    guardrail_status = GUARDRAIL_STATUS_MAP.get(raw_status, "not_run")
                    break

    return StandardLoggingPayloadStatusFields(
        llm_api_status=llm_api_status, guardrail_status=guardrail_status
    )

