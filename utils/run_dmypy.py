
def run_dmypy(args: list[str]) -> tuple[str, str, int]:
    from mypy.dmypy.client import main

    # A bunch of effort has been put into threading stdout and stderr
    # through the main API to avoid the threadsafety problems of
    # modifying sys.stdout/sys.stderr, but that hasn't been done for
    # the dmypy client, so we just do the non-threadsafe thing.
    def f(stdout: TextIO, stderr: TextIO) -> None:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        try:
            sys.stdout = stdout
            sys.stderr = stderr
            main(args)
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

    return _run(f)

