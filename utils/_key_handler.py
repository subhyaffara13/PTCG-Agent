
def _key_handler(event):
    # Dead reckoning of key.
    if event.name == "key_press_event":
        event.canvas._key = event.key
    elif event.name == "key_release_event":
        event.canvas._key = None

