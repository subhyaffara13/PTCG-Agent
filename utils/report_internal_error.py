import sys

def report_internal_error(
    err: Exception,
    file: str | None,
    line: int,
    errors: Errors | None,
    options: Options,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> NoReturn:
    """Report internal error and exit.

    This optionally starts pdb or shows a traceback.
    """
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    # Dump out errors so far, they often provide a clue.
    # But catch unexpected errors rendering them.
    if errors:
        try:
            for msg in errors.new_messages():
                print(msg)
        except Exception as e:
            print("Failed to dump errors:", repr(e), file=stderr)

    # Compute file:line prefix for official-looking error messages.
    if file:
        if line:
            prefix = f"{file}:{line}: "
        else:
            prefix = f"{file}: "
    else:
        prefix = ""

    # Print "INTERNAL ERROR" message.
    print(
        f"{prefix}error: INTERNAL ERROR --",
        "Please try using mypy master on GitHub:\n"
        "https://mypy.readthedocs.io/en/stable/common_issues.html"
        "#using-a-development-mypy-build",
        file=stderr,
    )
    if options.show_traceback:
        print("Please report a bug at https://github.com/python/mypy/issues", file=stderr)
    else:
        print(
            "If this issue continues with mypy master, "
            "please report a bug at https://github.com/python/mypy/issues",
            file=stderr,
        )
    print(f"version: {mypy_version}", file=stderr)

    # If requested, drop into pdb. This overrides show_tb.
    if options.pdb:
        print("Dropping into pdb", file=stderr)
        import pdb

        pdb.post_mortem(sys.exc_info()[2])

    # If requested, print traceback, else print note explaining how to get one.
    if options.raise_exceptions:
        raise err
    if not options.show_traceback:
        if not options.pdb:
            print(
                "{}note: please use --show-traceback to print a traceback "
                "when reporting a bug".format(prefix),
                file=stderr,
            )
    else:
        tberr = traceback.TracebackException.from_exception(err)
        tberr.stack[:0] = traceback.extract_stack()[:-2]
        print("".join(tberr.format()), file=stdout)
        print(f"{prefix}note: use --pdb to drop into pdb", file=stderr)

    # Exit.  The caller has nothing more to say.
    # We use exit code 2 to signal that this is no ordinary error.
    raise SystemExit(2)

