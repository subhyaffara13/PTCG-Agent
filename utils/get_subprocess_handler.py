
def get_subprocess_handler(
    entrypoint: str,
    args: tuple,
    env: dict[str, str],
    stdout: str,
    stderr: str,
    local_rank_id: int,
    numa_options: NumaOptions | None = None,
) -> SubprocessHandler:
    return SubprocessHandler(
        entrypoint=entrypoint,
        args=args,
        env=env,
        stdout=stdout,
        stderr=stderr,
        local_rank_id=local_rank_id,
        numa_options=numa_options,
    )

