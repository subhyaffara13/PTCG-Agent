
def _redact_model_response_dict_choices(choices, redacted_str: str):
    for choice in choices:
        if isinstance(choice, dict):
            if "message" in choice and isinstance(choice["message"], dict):
                choice["message"]["content"] = redacted_str
                if "reasoning_content" in choice["message"]:
                    choice["message"]["reasoning_content"] = redacted_str
                if "thinking_blocks" in choice["message"]:
                    choice["message"]["thinking_blocks"] = None
                if "audio" in choice["message"]:
                    choice["message"]["audio"] = None
            elif "delta" in choice and isinstance(choice["delta"], dict):
                choice["delta"]["content"] = redacted_str
                if "reasoning_content" in choice["delta"]:
                    choice["delta"]["reasoning_content"] = redacted_str
                if "thinking_blocks" in choice["delta"]:
                    choice["delta"]["thinking_blocks"] = None
                if "audio" in choice["delta"]:
                    choice["delta"]["audio"] = None
        else:
            _redact_choice_content(choice)

