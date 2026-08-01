
def arun_thread_stream(
    *,
    event_handler: Optional[AssistantEventHandler] = None,
    **kwargs,
) -> AsyncAssistantStreamManager[AsyncAssistantEventHandler]:
    kwargs["arun_thread"] = True
    return run_thread(stream=True, event_handler=event_handler, **kwargs)  # type: ignore

