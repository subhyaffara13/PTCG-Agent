
def get_selector() -> Selector:
    global _selector

    with _selector_lock:
        if _selector is None:
            _selector = Selector()
            _selector.start()

        return _selector

