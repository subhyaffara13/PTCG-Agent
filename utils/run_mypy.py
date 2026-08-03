import os
import re
import sys

def run_mypy() -> None:
    """Clears the cache and run mypy before running any of the typing tests.

    The mypy results are cached in `OUTPUT_MYPY` for further use.

    The cache refresh can be skipped using

    NUMPY_TYPING_TEST_CLEAR_CACHE=0 pytest numpy/typing/tests
    """
    if (
        os.path.isdir(CACHE_DIR)
        and bool(os.environ.get("NUMPY_TYPING_TEST_CLEAR_CACHE", True))
    ):
        shutil.rmtree(CACHE_DIR)

    split_pattern = re.compile(r"(\s+)?\^(\~+)?")
    for directory in (PASS_DIR, REVEAL_DIR, FAIL_DIR, MISC_DIR):
        # Run mypy
        stdout, stderr, exit_code = api.run([
            "--config-file",
            MYPY_INI,
            "--cache-dir",
            CACHE_DIR,
            directory,
        ])
        if stderr:
            pytest.fail(f"Unexpected mypy standard error\n\n{stderr}", False)
        elif exit_code not in {0, 1}:
            pytest.fail(f"Unexpected mypy exit code: {exit_code}\n\n{stdout}", False)

        str_concat = ""
        filename: str | None = None
        for i in stdout.split("\n"):
            if "note:" in i:
                continue
            if filename is None:
                filename = _key_func(i)

            str_concat += f"{i}\n"
            if split_pattern.match(i) is not None:
                OUTPUT_MYPY[filename].append(str_concat)
                str_concat = ""
                filename = None


def run_mypy(args: list[str]) -> None:
    __tracebackhide__ = True
    # We must enable site packages even though they could cause problems,
    # since stubs for typing_extensions live there.
    outval, errval, status = api.run(args + ["--show-traceback", "--no-silence-site-packages"])
    if status != 0:
        sys.stdout.write(outval)
        sys.stderr.write(errval)
        pytest.fail(reason="Sample check failed", pytrace=False)

