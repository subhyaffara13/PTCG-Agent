
def get_function_event(function_events, partial_event_name):
    """
    Returns the first event that matches partial_event_name in the provided
    function_events. These function_events should be the output of
    torch.autograd.profiler.function_events().

    Args:
    function_events: function_events returned by the profiler.
    event_name (str): partial key that the event was profiled with.
    """
    event = [event for event in function_events if partial_event_name in event.name][0]  # noqa: RUF015
    return event

