
def check_python_version(program: str) -> None:
    """Report issues with the Python used to run mypy, dmypy, or stubgen"""
    # Check for known bad Python versions.
    if sys.version_info[:2] < (3, 10):  # noqa: UP036, RUF100
        sys.exit(
            "Running {name} with Python 3.9 or lower is not supported; "
            "please upgrade to 3.10 or newer".format(name=program)
        )

