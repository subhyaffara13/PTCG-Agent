
def register_event(event_name: EventName):
    """A class decorator to register an EventName for an Action class."""

    def decorator(cls):
        ACTION_EVENT_MAP[cls.__name__] = event_name
        setattr(cls, "event_name", event_name)
        return cls

    return decorator

