
def validate_vertex_input(
    input_data: VertexInput, kwargs: dict, optional_params: dict
) -> None:
    # Remove None values
    if input_data.get("text") is None:
        input_data.pop("text", None)
    if input_data.get("ssml") is None:
        input_data.pop("ssml", None)

    # Check if use_ssml is set
    use_ssml = kwargs.get("use_ssml", optional_params.get("use_ssml", False))

    if use_ssml:
        if "text" in input_data:
            input_data["ssml"] = input_data.pop("text")
        elif "ssml" not in input_data:
            raise ValueError("SSML input is required when use_ssml is True.")
    else:
        # LiteLLM will auto-detect if text is in ssml format
        # check if "text" is an ssml - in this case we should pass it as ssml instead of text
        if input_data:
            _text = input_data.get("text", None) or ""
            if "<speak>" in _text:
                input_data["ssml"] = input_data.pop("text")

    if not input_data:
        raise ValueError("Either 'text' or 'ssml' must be provided.")
    if "text" in input_data and "ssml" in input_data:
        raise ValueError("Only one of 'text' or 'ssml' should be provided, not both.")

