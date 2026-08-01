
def test_event(name: str, *args) -> None:
  if not test_event_listener:
    return
  test_event_listener(name, *args)

