from typing import Any

def _set_weave_specific_attributes(
    span: Span, kwargs: dict[str, Any], response_obj: Any
):
    """
    Sets Weave-specific metadata attributes onto the OTEL span.

    Based on Weave's OTEL attribute mappings from:
    https://github.com/wandb/weave/blob/master/weave/trace_server/opentelemetry/constants.py
    """

    # Extract all needed data upfront
    litellm_params = kwargs.get("litellm_params") or {}
    # optional_params = kwargs.get("optional_params") or {}
    metadata = kwargs.get("metadata") or {}
    model = kwargs.get("model") or ""
    custom_llm_provider = litellm_params.get("custom_llm_provider") or ""

    # Weave supports a custom display name and will default to the model name if not provided.
    display_name = metadata.get("display_name")
    if not display_name and model:
        if custom_llm_provider:
            display_name = f"{custom_llm_provider}/{model}"
        else:
            display_name = model
    if display_name:
        display_name = display_name.replace("/", "__")
        safe_set_attribute(span, WeaveSpanAttributes.DISPLAY_NAME.value, display_name)

    # Weave threads are OpenInference sessions.
    if (session_id := metadata.get("session_id")) is not None:
        if isinstance(session_id, (list, dict)):
            session_id = safe_dumps(session_id)
        safe_set_attribute(span, WeaveSpanAttributes.THREAD_ID.value, session_id)
        safe_set_attribute(span, WeaveSpanAttributes.IS_TURN.value, True)

    # Response attributes are already set by _utils.set_attributes,
    # but we override them here to better match Weave's expectations
    if response_obj:
        output_dict = None
        if hasattr(response_obj, "model_dump"):
            output_dict = response_obj.model_dump()
        elif hasattr(response_obj, "get"):
            output_dict = response_obj

        if output_dict:
            safe_set_attribute(
                span, OpenInferenceSpanAttributes.OUTPUT_VALUE, safe_dumps(output_dict)
            )

