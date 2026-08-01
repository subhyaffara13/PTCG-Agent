
def maybe_wrap_pytest_function_for_tracing(pyfuncitem) -> None:
    """Wrap the given pytestfunct item for tracing support if --trace was given in
    the command line."""
    if pyfuncitem.config.getvalue("trace"):
        wrap_pytest_function_for_tracing(pyfuncitem)

