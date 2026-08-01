
def verify_ddp_error_logged(model_DDP, err_substr):
    # Verify error was logged in ddp_logging_data.
    ddp_logging_data = model_DDP._get_ddp_logging_data()
    if "iteration" not in ddp_logging_data:
        raise AssertionError("Expected 'iteration' in ddp_logging_data")
    if "has_error" not in ddp_logging_data:
        raise AssertionError("Expected 'has_error' in ddp_logging_data")
    if "error" not in ddp_logging_data:
        raise AssertionError("Expected 'error' in ddp_logging_data")
    logging_err = ddp_logging_data["error"]
    # Remove C++ stacktrace if needed.
    actual = (
        err_substr
        if err_substr.find("\nException raised from ") == -1
        else err_substr.split("\nException raised from ")[0]
    )
    if actual not in logging_err:
        raise AssertionError(
            f"Did not find expected {actual} in ddp logging data error: {logging_err}"
        )

