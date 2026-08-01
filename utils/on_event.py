
def on_event(event_type: EventName):
    def decorator(func):
        setattr(func, EVENT_HANDLER_FOR_ATTR_NAME, event_type)
        return func

    return decorator

