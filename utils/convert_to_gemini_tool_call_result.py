import json
from typing import List, Optional, Union

def convert_to_gemini_tool_call_result(
    message: Union[ChatCompletionToolMessage, ChatCompletionFunctionMessage],
    last_message_with_tool_calls: Optional[dict],
    model: Optional[str] = None,
    custom_llm_provider: Optional[str] = None,
) -> Union[VertexPartType, List[VertexPartType]]:
    """
    OpenAI message with a tool result looks like:
    {
        "tool_call_id": "tool_1",
        "role": "tool",
        "content": "function result goes here",
    },

    # NOTE: Function messages have been deprecated
    OpenAI message with a function call result looks like:
    {
        "role": "function",
        "name": "get_current_weather",
        "content": "function result goes here",
    }

    Supports content with images for Computer Use:
    {
        "role": "tool",
        "tool_call_id": "call_abc123",
        "content": [
            {"type": "text",       "text": "I found the requested image:"},
            {"type": "input_image", "image_url": "https://example.com/image.jpg" }
        ]
    }
    """
    from litellm.types.llms.vertex_ai import BlobType

    content_str: str = ""
    inline_data_list: List[BlobType] = []

    if "content" in message:
        if isinstance(message["content"], str):
            content_str = message["content"]
            # Detect data-URL images (e.g. from Anthropic tool_result with a single image block
            # that was serialised as a plain string by translate_anthropic_messages_to_openai)
            # and promote them to inline_data so Gemini receives actual image bytes.
            if content_str[:5].lower() == "data:" and ";base64," in content_str:
                try:
                    mime_rest = content_str[5:].split(";base64,", 1)
                    if len(mime_rest) == 2 and mime_rest[0].startswith("image/"):
                        # Strip any extra parameters (e.g. ";charset=UTF-8") from the MIME segment
                        clean_mime = mime_rest[0].split(";")[0].strip()
                        inline_data_list.append(
                            BlobType(data=mime_rest[1], mime_type=clean_mime)
                        )
                        content_str = ""
                except Exception as e:
                    verbose_logger.warning(
                        f"Failed to parse data URL in tool response: {e}"
                    )
        elif isinstance(message["content"], List):
            content_list = message["content"]
            for content in content_list:
                content_type = content.get("type", "")
                if content_type == "text":
                    content_str += content.get("text", "")
                elif content_type == "image":
                    # Anthropic-native image block: {"type": "image", "source": {"type": "base64", ...}}
                    source = content.get("source", {})
                    if isinstance(source, dict) and source.get("type") == "base64":
                        try:
                            inline_data_list.append(
                                BlobType(
                                    data=source.get("data", ""),
                                    mime_type=source.get("media_type", "image/jpeg"),
                                )
                            )
                        except Exception as e:
                            verbose_logger.warning(
                                f"Failed to process Anthropic image block in tool response: {e}"
                            )
                elif content_type in ("input_image", "image_url"):
                    # Extract image for inline_data (for Computer Use screenshots and tool results)
                    image_url_data = content.get("image_url", "")
                    image_url = (
                        image_url_data.get("url", "")
                        if isinstance(image_url_data, dict)
                        else image_url_data
                    )

                    if image_url:
                        # Convert image to base64 blob format for Gemini
                        try:
                            image_obj = convert_to_anthropic_image_obj(
                                image_url, format=None
                            )
                            inline_data_list.append(
                                BlobType(
                                    data=image_obj["data"],
                                    mime_type=image_obj["media_type"],
                                )
                            )
                        except Exception as e:
                            verbose_logger.warning(
                                f"Failed to process image in tool response: {e}"
                            )
                elif content_type in ("file", "input_file"):
                    # Extract file for inline_data (for tool results with PDF, audio, video, etc.)
                    file_data = content.get("file_data", "")
                    if not file_data:
                        file_content = content.get("file", {})
                        file_data = (
                            file_content.get("file_data", "")
                            if isinstance(file_content, dict)
                            else file_content if isinstance(file_content, str) else ""
                        )

                    if file_data:
                        # Convert file to base64 blob format for Gemini
                        try:
                            file_obj = convert_to_anthropic_image_obj(
                                file_data, format=None
                            )
                            inline_data_list.append(
                                BlobType(
                                    data=file_obj["data"],
                                    mime_type=file_obj["media_type"],
                                )
                            )
                        except Exception as e:
                            verbose_logger.warning(
                                f"Failed to process file in tool response: {e}"
                            )
    name: Optional[str] = message.get("name", "")  # type: ignore

    # Recover name from last message with tool calls
    if last_message_with_tool_calls:
        tools = last_message_with_tool_calls.get("tool_calls", [])
        msg_tool_call_id = message.get("tool_call_id", None)
        for tool in tools:
            prev_tool_call_id = tool.get("id", None)
            if (
                msg_tool_call_id
                and prev_tool_call_id
                and msg_tool_call_id == prev_tool_call_id
            ):
                name = tool.get("function", {}).get("name", "")

    # Echo the OpenAI tool_call_id on functionResponse (strip thought-signature suffix).
    # Only Google AI Studio Gemini 3+ accepts `id` on function_response parts.
    # Vertex AI and older Gemini models reject the field with HTTP 400.
    from litellm.llms.vertex_ai.gemini.vertex_and_google_ai_studio_gemini import (
        VertexGeminiConfig,
    )

    gemini_call_id: Optional[str] = None
    if model and VertexGeminiConfig._forward_gemini_function_call_id(
        model, custom_llm_provider
    ):
        raw_tool_call_id = message.get("tool_call_id")
        if raw_tool_call_id and isinstance(raw_tool_call_id, str):
            stripped_id = raw_tool_call_id.split(THOUGHT_SIGNATURE_SEPARATOR, 1)[0]
            if stripped_id:
                gemini_call_id = stripped_id

    if not name:
        raise Exception(
            "Missing corresponding tool call for tool response message. Received - message={}, last_message_with_tool_calls={}".format(
                message, last_message_with_tool_calls
            )
        )

    # Parse response data - support both JSON string and plain string
    # For Computer Use, the response should contain structured data like {"url": "..."}
    response_data: dict
    try:
        if content_str.strip().startswith("{") or content_str.strip().startswith("["):
            # Try to parse as JSON (for Computer Use structured responses)
            parsed = json.loads(content_str)
            if isinstance(parsed, dict):
                response_data = parsed  # Use the parsed JSON directly
            else:
                response_data = {"content": content_str}
        else:
            response_data = {"content": content_str}
    except (json.JSONDecodeError, ValueError):
        # Not valid JSON, wrap in content field
        response_data = {"content": content_str}

    # We can't determine from openai message format whether it's a successful or
    # error call result so default to the successful result template
    _function_response = VertexFunctionResponse(
        name=name,
        response=response_data,  # type: ignore
    )
    if gemini_call_id:
        _function_response["id"] = gemini_call_id

    _part: VertexPartType = {"function_response": _function_response}

    # For multimodal function responses, Gemini expects media parts nested
    # inside functionResponse.parts instead of sibling content parts.
    if inline_data_list:
        _function_response["parts"] = [
            {"inline_data": inline_data} for inline_data in inline_data_list
        ]
        return [_part]

    return _part

