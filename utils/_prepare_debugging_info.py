
def _prepare_debugging_info(test_info, info):
    """Combine the information about the test and the call information to a patched function/method within it."""

    info = f"{test_info}\n\n{info}"
    p = os.path.join(os.environ.get("_PATCHED_TESTING_METHODS_OUTPUT_DIR", ""), "captured_info.txt")
    # TODO (ydshieh): This is not safe when we use pytest-xdist with more than 1 worker.
    with open(p, "a") as fp:
        fp.write(f"{info}\n\n{'=' * 120}\n\n")

    return info

