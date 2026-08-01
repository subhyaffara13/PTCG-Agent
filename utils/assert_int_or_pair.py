
def assert_int_or_pair(arg: list[int], arg_name: str, message: str) -> None:
    if not (isinstance(arg, int) or len(arg) == 2):
        raise AssertionError(message.format(arg_name))

