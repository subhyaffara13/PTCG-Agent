from typing import Any

def _patch_logging_obj_for_guardrail(
    litellm_logging_obj: Any, request: ApplyGuardrailRequest
) -> None:
    """Configure the logging object so Langfuse/OTEL extract input and output correctly."""
    litellm_logging_obj.call_type = "pass_through_endpoint"
    litellm_logging_obj.model_call_details["call_type"] = "pass_through_endpoint"
    litellm_logging_obj.update_messages(
        request.messages
        if request.messages
        else [{"role": "user", "content": request.text}]
    )

