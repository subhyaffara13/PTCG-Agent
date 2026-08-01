
def get_non_default_transcription_params(kwargs: dict) -> dict:
    from litellm.constants import OPENAI_TRANSCRIPTION_PARAMS

    default_params = OPENAI_TRANSCRIPTION_PARAMS + all_litellm_params
    non_default_params = {k: v for k, v in kwargs.items() if k not in default_params}
    return non_default_params

