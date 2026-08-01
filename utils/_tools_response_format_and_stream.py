
def _tools_response_format_and_stream(
    optional_params: dict, model_params: dict
) -> Tuple[dict, dict, dict]:
    tools_ = optional_params.pop("tools", [])
    tools_ = [validate_dict(tool, ChatCompletionTool) for tool in tools_]
    tools: dict = {"tools": tools_} if tools_ else {}

    response_format = model_params.pop("response_format", {})
    resp_type = response_format.get("type", None)
    if resp_type:
        if resp_type == "json_schema":
            response_format = validate_dict(response_format, ResponseFormatJSONSchema)
        else:
            response_format = validate_dict(response_format, ResponseFormat)
        response_format = {"response_format": response_format}

    model_params.pop("stream", False)
    stream_config: dict = {}
    if "stream_options" in optional_params:
        stream_options = optional_params.pop("stream_options", {})
        if "chunk_size" in stream_options:
            stream_config["chunk_size"] = stream_options.get("chunk_size")
        if "delimiters" in stream_options:
            stream_config["delimiters"] = stream_options.get("delimiters")

    return tools, response_format, stream_config

