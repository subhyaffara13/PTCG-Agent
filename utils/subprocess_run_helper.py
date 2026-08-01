
def subprocess_run_helper(func, *args, timeout, extra_env=None):
    """
    Run a function in a sub-process.

    Parameters
    ----------
    func : function
        The function to be run.  It must be in a module that is importable.
    *args : str
        Any additional command line arguments to be passed in
        the first argument to ``subprocess.run``.
    extra_env : dict[str, str]
        Any additional environment variables to be set for the subprocess.
    """
    target = func.__name__
    module = func.__module__
    file = func.__code__.co_filename
    proc = subprocess_run_for_testing(
        [
            sys.executable,
            "-c",
            f"import importlib.util;"
            f"_spec = importlib.util.spec_from_file_location({module!r}, {file!r});"
            f"_module = importlib.util.module_from_spec(_spec);"
            f"_spec.loader.exec_module(_module);"
            f"_module.{target}()",
            *args,
        ],
        env={
            **os.environ,
            "SOURCE_DATE_EPOCH": "0",
            # subprocess_run_helper sets SOURCE_DATE_EPOCH=0 above, so for a dirty tree,
            # the version will have the date 19700101 which breaks pickle tests with a
            # warning if the working tree is dirty.
            #
            # This will also avoid at least one additional subprocess call for
            # setuptools-scm query git, so we tell the subprocess what version
            # to report as the test process.
            "SETUPTOOLS_SCM_PRETEND_VERSION_FOR_MATPLOTLIB": mpl.__version__,
            **(extra_env or {}),
        },
        timeout=timeout,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return proc

