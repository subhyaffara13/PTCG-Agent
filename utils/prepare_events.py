
def prepare_events(events):
    """Standardize event functions and extract attributes."""
    if callable(events):
        events = (events,)

    max_events = np.empty(len(events))
    direction = np.empty(len(events))
    for i, event in enumerate(events):
        terminal = getattr(event, 'terminal', None)
        direction[i] = getattr(event, 'direction', 0)

        message = ('The `terminal` attribute of each event '
                   'must be a boolean or positive integer.')
        if terminal is None or terminal == 0:
            max_events[i] = np.inf
        elif int(terminal) == terminal and terminal > 0:
            max_events[i] = terminal
        else:
            raise ValueError(message)

    return events, max_events, direction

