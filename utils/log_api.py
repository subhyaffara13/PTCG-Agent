
def log_api(**kwargs):
    exit_stack = contextlib.ExitStack()
    exit_stack.enter_context(preserve_log_state())
    torch._logging.set_logs(**kwargs)
    return exit_stack

