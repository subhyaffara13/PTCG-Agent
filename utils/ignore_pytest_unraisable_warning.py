
def ignore_pytest_unraisable_warning(f):
    unraisable = "PytestUnraisableExceptionWarning"
    if hasattr(pytest, unraisable):  # Python >= 3.8 and pytest >= 6
        dec = pytest.mark.filterwarnings(f"ignore::pytest.{unraisable}")
        return dec(f)
    return f

