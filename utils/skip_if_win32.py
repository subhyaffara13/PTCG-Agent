
def skip_if_win32():
    return skip_but_pass_in_sandcastle_if(
        sys.platform == "win32",
        "This unit test case is not supported on Windows platform",
    )

