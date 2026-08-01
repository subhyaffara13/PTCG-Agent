
def drain_queue(request_queue: queue.Queue) -> list[RequestState]:
    """Drains a queue and returns a list of RequestStates."""
    new_states: list[RequestState] = []
    while not request_queue.empty():
        try:
            state = request_queue.get_nowait()
            if state is not None:
                new_states.append(state)
        except queue.Empty:
            break
    return new_states

