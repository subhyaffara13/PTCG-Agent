
def _except_handlers_ignores_exceptions(
    handlers: nodes.ExceptHandler,
    exceptions: tuple[type[ImportError], type[ModuleNotFoundError]],
) -> bool:
    func = partial(error_of_type, error_type=exceptions)
    return any(func(handler) for handler in handlers)

