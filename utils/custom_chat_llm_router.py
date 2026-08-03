from typing import Optional

def custom_chat_llm_router(
    async_fn: bool, stream: Optional[bool], custom_llm: CustomLLM
):
    """
    Routes call to CustomLLM completion/acompletion/streaming/astreaming functions, based on call type

    Validates if response is in expected format
    """
    if async_fn:
        if stream:
            return custom_llm.astreaming
        return custom_llm.acompletion
    if stream:
        return custom_llm.streaming
    return custom_llm.completion

