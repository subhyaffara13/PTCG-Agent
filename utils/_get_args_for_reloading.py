
def _get_args_for_reloading() -> list[str]:
    """Determine how the script was executed, and return the args needed
    to execute it again in a new process.
    """
    if sys.version_info >= (3, 10):
        # sys.orig_argv, added in Python 3.10, contains the exact args used to invoke
        # Python. Still replace argv[0] with sys.executable for accuracy.
        return [sys.executable, *sys.orig_argv[1:]]

    rv = [sys.executable]
    py_script = sys.argv[0]
    args = sys.argv[1:]
    # Need to look at main module to determine how it was executed.
    __main__ = sys.modules["__main__"]

    # The value of __package__ indicates how Python was called. It may
    # not exist if a setuptools script is installed as an egg. It may be
    # set incorrectly for entry points created with pip on Windows.
    if getattr(__main__, "__package__", None) is None or (
        os.name == "nt"
        and __main__.__package__ == ""
        and not os.path.exists(py_script)
        and os.path.exists(f"{py_script}.exe")
    ):
        # Executed a file, like "python app.py".
        py_script = os.path.abspath(py_script)

        if os.name == "nt":
            # Windows entry points have ".exe" extension and should be
            # called directly.
            if not os.path.exists(py_script) and os.path.exists(f"{py_script}.exe"):
                py_script += ".exe"

            if (
                os.path.splitext(sys.executable)[1] == ".exe"
                and os.path.splitext(py_script)[1] == ".exe"
            ):
                rv.pop(0)

        rv.append(py_script)
    else:
        # Executed a module, like "python -m werkzeug.serving".
        if os.path.isfile(py_script):
            # Rewritten by Python from "-m script" to "/path/to/script.py".
            py_module = t.cast(str, __main__.__package__)
            name = os.path.splitext(os.path.basename(py_script))[0]

            if name != "__main__":
                py_module += f".{name}"
        else:
            # Incorrectly rewritten by pydevd debugger from "-m script" to "script".
            py_module = py_script

        rv.extend(("-m", py_module.lstrip(".")))

    rv.extend(args)
    return rv

