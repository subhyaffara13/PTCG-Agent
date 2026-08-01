
def log_provider_specific_information_as_span(
    trace,
    clean_metadata,
):
    """
    Logs provider-specific information as spans.

    Parameters:
        trace: The tracing object used to log spans.
        clean_metadata: A dictionary containing metadata to be logged.

    Returns:
        None
    """

    _hidden_params = clean_metadata.get("hidden_params", None)
    if _hidden_params is None:
        return

    vertex_ai_grounding_metadata = _hidden_params.get(
        "vertex_ai_grounding_metadata", None
    )

    if vertex_ai_grounding_metadata is not None:
        if isinstance(vertex_ai_grounding_metadata, list):
            for elem in vertex_ai_grounding_metadata:
                if isinstance(elem, dict):
                    for key, value in elem.items():
                        trace.span(
                            name=key,
                            input=value,
                        )
                else:
                    trace.span(
                        name="vertex_ai_grounding_metadata",
                        input=elem,
                    )
        else:
            trace.span(
                name="vertex_ai_grounding_metadata",
                input=vertex_ai_grounding_metadata,
            )

