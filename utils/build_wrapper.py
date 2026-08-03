import functools
from typing import Callable

def build_wrapper(func: Callable[P, R], event_handlers: list[BaseValidateHandlerProtocol]) -> Callable[P, R]:
    if not event_handlers:
        return func
    else:
        on_enters = tuple(h.on_enter for h in event_handlers if filter_handlers(h, 'on_enter'))
        on_successes = tuple(h.on_success for h in event_handlers if filter_handlers(h, 'on_success'))
        on_errors = tuple(h.on_error for h in event_handlers if filter_handlers(h, 'on_error'))
        on_exceptions = tuple(h.on_exception for h in event_handlers if filter_handlers(h, 'on_exception'))

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for on_enter_handler in on_enters:
                on_enter_handler(*args, **kwargs)

            try:
                result = func(*args, **kwargs)
            except ValidationError as error:
                for on_error_handler in on_errors:
                    on_error_handler(error)
                raise
            except Exception as exception:
                for on_exception_handler in on_exceptions:
                    on_exception_handler(exception)
                raise
            else:
                for on_success_handler in on_successes:
                    on_success_handler(result)
                return result

        return wrapper

