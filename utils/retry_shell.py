
def retry_shell(
    command,
    cwd=None,
    env=None,
    stdout=None,
    stderr=None,
    timeout=None,
    retries=1,
    was_rerun=False,
) -> tuple[int, bool]:
    # Returns exicode + whether it was rerun
    if not (retries >= 0):
        raise AssertionError(
            f"Expecting non negative number for number of retries, got {retries}"
        )
    try:
        exit_code = shell(
            command, cwd=cwd, env=env, stdout=stdout, stderr=stderr, timeout=timeout
        )
        if exit_code == 0 or retries == 0:
            return exit_code, was_rerun
        print(
            f"Got exit code {exit_code}, retrying (retries left={retries})",
            file=stdout,
            flush=True,
        )
    except subprocess.TimeoutExpired:
        if retries == 0:
            print(
                f"Command took >{timeout // 60}min, returning 124",
                file=stdout,
                flush=True,
            )
            return 124, was_rerun
        print(
            f"Command took >{timeout // 60}min, retrying (retries left={retries})",
            file=stdout,
            flush=True,
        )
    return retry_shell(
        command,
        cwd=cwd,
        env=env,
        stdout=stdout,
        stderr=stderr,
        timeout=timeout,
        retries=retries - 1,
        was_rerun=True,
    )

