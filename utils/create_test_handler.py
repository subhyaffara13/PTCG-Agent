
def create_test_handler(
    handler_class: type[CheckpointableHandler[T, AbstractT]],
    **kwargs,
) -> _TestHandler[T, AbstractT]:
  return _TestHandler[T, AbstractT](handler_class, **kwargs)

