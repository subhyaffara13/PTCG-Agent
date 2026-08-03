from typing import Optional

def add_guardrail_response_to_standard_logging_object(
    litellm_logging_obj: Optional["LiteLLMLogging"],
    guardrail_response: StandardLoggingGuardrailInformation,
):
    if litellm_logging_obj is None:
        return
    standard_logging_object: Optional[StandardLoggingPayload] = (
        litellm_logging_obj.model_call_details.get("standard_logging_object")
    )
    if standard_logging_object is None:
        return
    guardrail_information = standard_logging_object.get("guardrail_information", [])
    if guardrail_information is None:
        guardrail_information = []
    guardrail_information.append(guardrail_response)
    standard_logging_object["guardrail_information"] = guardrail_information

    return standard_logging_object

