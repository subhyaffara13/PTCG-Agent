from typing import Any, Optional

def _add_prompt_to_generation_params(
    generation_params: dict,
    clean_metadata: dict,
    prompt_management_metadata: Optional[StandardLoggingPromptManagementMetadata],
    langfuse_client: Any,
) -> dict:
    from langfuse import Langfuse
    from langfuse.model import (
        ChatPromptClient,
        Prompt_Chat,
        Prompt_Text,
        TextPromptClient,
    )

    langfuse_client = cast(Langfuse, langfuse_client)

    user_prompt = clean_metadata.pop("prompt", None)
    if user_prompt is None and prompt_management_metadata is None:
        pass
    elif isinstance(user_prompt, dict):
        if user_prompt.get("type", "") == "chat":
            _prompt_chat = Prompt_Chat(**user_prompt)
            generation_params["prompt"] = ChatPromptClient(prompt=_prompt_chat)
        elif user_prompt.get("type", "") == "text":
            _prompt_text = Prompt_Text(**user_prompt)
            generation_params["prompt"] = TextPromptClient(prompt=_prompt_text)
        elif "version" in user_prompt and "prompt" in user_prompt:
            # prompts
            if isinstance(user_prompt["prompt"], str):
                prompt_text_params = getattr(
                    Prompt_Text, "model_fields", Prompt_Text.__fields__
                )
                _data = {
                    "name": user_prompt["name"],
                    "prompt": user_prompt["prompt"],
                    "version": user_prompt["version"],
                    "config": user_prompt.get("config", None),
                }
                if "labels" in prompt_text_params and "tags" in prompt_text_params:
                    _data["labels"] = user_prompt.get("labels", []) or []
                    _data["tags"] = user_prompt.get("tags", []) or []
                _prompt_obj = Prompt_Text(**_data)  # type: ignore
                generation_params["prompt"] = TextPromptClient(prompt=_prompt_obj)

            elif isinstance(user_prompt["prompt"], list):
                prompt_chat_params = getattr(
                    Prompt_Chat, "model_fields", Prompt_Chat.__fields__
                )
                _data = {
                    "name": user_prompt["name"],
                    "prompt": user_prompt["prompt"],
                    "version": user_prompt["version"],
                    "config": user_prompt.get("config", None),
                }
                if "labels" in prompt_chat_params and "tags" in prompt_chat_params:
                    _data["labels"] = user_prompt.get("labels", []) or []
                    _data["tags"] = user_prompt.get("tags", []) or []

                _prompt_obj = Prompt_Chat(**_data)  # type: ignore

                generation_params["prompt"] = ChatPromptClient(prompt=_prompt_obj)
            else:
                verbose_logger.error(
                    "[Non-blocking] Langfuse Logger: Invalid prompt format"
                )
        else:
            verbose_logger.error(
                "[Non-blocking] Langfuse Logger: Invalid prompt format. No prompt logged to Langfuse"
            )
    elif (
        prompt_management_metadata is not None
        and prompt_management_metadata["prompt_integration"] == "langfuse"
    ):
        try:
            generation_params["prompt"] = langfuse_client.get_prompt(
                prompt_management_metadata["prompt_id"]
            )
        except Exception as e:
            verbose_logger.debug(
                f"[Non-blocking] Langfuse Logger: Error getting prompt client for logging: {e}"
            )
            pass

    else:
        generation_params["prompt"] = user_prompt

    return generation_params

