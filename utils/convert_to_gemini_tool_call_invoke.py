
def convert_to_gemini_tool_call_invoke(
    message: ChatCompletionAssistantMessage,
    model: Optional[str] = None,
    custom_llm_provider: Optional[str] = None,
) -> List[VertexPartType]:
    """
    OpenAI tool invokes:
    {
      "role": "assistant",
      "content": null,
      "tool_calls": [
        {
          "id": "call_abc123",
          "type": "function",
          "function": {
            "name": "get_current_weather",
            "arguments": "{\n\"location\": \"Boston, MA\"\n}"
          }
        }
      ]
    },
    """
    """
    Gemini tool call invokes:
    {
      "role": "model",
      "parts": [
        {
          "functionCall": {
            "name": "get_current_weather",
            "args": {
              "unit": "fahrenheit",
              "predicted_temperature": 45,
              "location": "Boston, MA",
            }
          }
        }
      ]
    }
    """

    """
    - json.load the arguments
    """
    try:
        _parts_list: List[VertexPartType] = []
        tool_calls = message.get("tool_calls", None)
        function_call = message.get("function_call", None)

        from litellm.llms.vertex_ai.gemini.vertex_and_google_ai_studio_gemini import (
            VertexGeminiConfig,
        )

        forward_tool_call_id = bool(
            model
            and VertexGeminiConfig._forward_gemini_function_call_id(
                model, custom_llm_provider
            )
        )

        if tool_calls is not None:
            for idx, tool in enumerate(tool_calls):
                if "function" in tool:
                    gemini_function_call: Optional[VertexFunctionCall] = (
                        _gemini_tool_call_invoke_helper(
                            function_call_params=tool["function"],
                            tool_call_id=(
                                tool.get("id") if forward_tool_call_id else None
                            ),
                        )
                    )
                    if gemini_function_call is not None:
                        part_dict: VertexPartType = {
                            "function_call": gemini_function_call
                        }
                        thought_signature = _get_thought_signature_from_tool(
                            dict(tool), model=model
                        )
                        if thought_signature:
                            part_dict["thoughtSignature"] = thought_signature

                        _parts_list.append(part_dict)
                    else:  # don't silently drop params. Make it clear to user what's happening.
                        raise Exception(
                            "function_call missing. Received tool call with 'type': 'function'. No function call in argument - {}".format(
                                tool
                            )
                        )
        elif function_call is not None:
            gemini_function_call = _gemini_tool_call_invoke_helper(
                function_call_params=function_call
            )
            if gemini_function_call is not None:
                part_dict_function: VertexPartType = {
                    "function_call": gemini_function_call
                }

                # Extract thought signature from function_call's provider_specific_fields
                thought_signature = None
                provider_fields = (
                    function_call.get("provider_specific_fields")
                    if isinstance(function_call, dict)
                    else {}
                )
                if isinstance(provider_fields, dict):
                    thought_signature = provider_fields.get("thought_signature")

                # If no signature found and model is gemini-3, use dummy signature
                if (
                    not thought_signature
                    and model
                    and VertexGeminiConfig._is_gemini_3_or_newer(model)
                ):
                    thought_signature = _get_dummy_thought_signature()

                if thought_signature:
                    part_dict_function["thoughtSignature"] = thought_signature

                _parts_list.append(part_dict_function)
            else:  # don't silently drop params. Make it clear to user what's happening.
                raise Exception(
                    "function_call missing. Received tool call with 'type': 'function'. No function call in argument - {}".format(
                        message
                    )
                )
        return _parts_list
    except Exception as e:
        raise Exception(
            "Unable to convert openai tool calls={} to gemini tool calls. Received error={}".format(
                message, str(e)
            )
        )

