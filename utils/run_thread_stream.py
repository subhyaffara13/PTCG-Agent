from typing import Optional

def run_thread_stream(
    *,
    event_handler: Optional[AssistantEventHandler] = None,
    **kwargs,
) -> AssistantStreamManager[AssistantEventHandler]:
    return run_thread(stream=True, event_handler=event_handler, **kwargs)  # type: ignore

