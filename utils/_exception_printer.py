
def _exception_printer(exc):
    if _get_running_interactive_framework() in ["headless", None]:
        raise exc
    else:
        traceback.print_exc()

