
def get_search_dirs(python_executable: str | None) -> tuple[list[str], list[str]]:
    """Find package directories for given python. Guaranteed to return absolute paths.

    This runs a subprocess call, which generates a list of the directories in sys.path.
    To avoid repeatedly calling a subprocess (which can be slow!) we
    lru_cache the results.
    """

    if python_executable is None:
        return ([], [])
    elif python_executable == sys.executable:
        # Use running Python's package dirs
        sys_path, site_packages = pyinfo.getsearchdirs()
    else:
        # Use subprocess to get the package directory of given Python
        # executable
        env = {**dict(os.environ), "PYTHONSAFEPATH": "1"}
        try:
            sys_path, site_packages = ast.literal_eval(
                subprocess.check_output(
                    [python_executable, pyinfo.__file__, "getsearchdirs"],
                    env=env,
                    stderr=subprocess.PIPE,
                ).decode()
            )
        except subprocess.CalledProcessError as err:
            print(err.stderr)
            print(err.stdout)
            raise
        except OSError as err:
            assert err.errno is not None
            reason = os.strerror(err.errno)
            raise CompileError(
                [f"mypy: Invalid python executable '{python_executable}': {reason}"]
            ) from err
    return sys_path, site_packages

