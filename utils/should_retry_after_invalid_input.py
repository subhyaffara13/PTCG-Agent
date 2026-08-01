
def should_retry_after_invalid_input(
    func: Callable[_P, _ReturnValueT],
) -> Callable[_P, _ReturnValueT]:
    """Decorator that handles InvalidUserInput exceptions and retries."""

    def inner_function(*args: _P.args, **kwargs: _P.kwargs) -> _ReturnValueT:
        called_once = False
        while True:
            try:
                return func(*args, **kwargs)
            except InvalidUserInput as exc:
                if called_once and exc.input == "exit()":
                    print("Stopping 'pylint-config'.")
                    sys.exit()
                print(f"Answer should be one of {exc.valid}.")
                print("Type 'exit()' if you want to exit the program.")
                called_once = True

    return inner_function

