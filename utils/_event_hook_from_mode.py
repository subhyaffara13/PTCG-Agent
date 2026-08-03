from typing import Union

def _event_hook_from_mode(
    mode: str | list[str] | Mode,
) -> Union[GuardrailEventHooks, list[GuardrailEventHooks], Mode]:
    if isinstance(mode, Mode):
        return mode
    if isinstance(mode, list):
        return [GuardrailEventHooks(item) for item in mode]
    return GuardrailEventHooks(mode)

