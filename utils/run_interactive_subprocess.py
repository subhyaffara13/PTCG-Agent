
def run_interactive_subprocess(
    command: str | list[str],
    folder: str | Path | None = None,
    **kwargs,
) -> Generator[tuple[IO[str], IO[str]], None, None]:
    """Run a subprocess in an interactive mode in a context manager.

    Args:
        command (`str` or `list[str]`):
            The command to execute as a string or list of strings.
        folder (`str`, *optional*):
            The folder in which to run the command. Defaults to current working
            directory (from `os.getcwd()`).
        kwargs (`dict[str]`):
            Keyword arguments to be passed to the `subprocess.run` underlying command.

    Returns:
        `tuple[IO[str], IO[str]]`: A tuple with `stdin` and `stdout` to interact
        with the process (input and output are utf-8 encoded).

    Example:
    ```python
    with _interactive_subprocess("git credential-store get") as (stdin, stdout):
        # Write to stdin
        stdin.write("url=hf.co\nusername=obama\n".encode("utf-8"))
        stdin.flush()

        # Read from stdout
        output = stdout.read().decode("utf-8")
    ```
    """
    if isinstance(command, str):
        command = command.split()

    with subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace",  # if not utf-8, replace char by �
        cwd=folder or os.getcwd(),
        **kwargs,
    ) as process:
        assert process.stdin is not None, "subprocess is opened as subprocess.PIPE"
        assert process.stdout is not None, "subprocess is opened as subprocess.PIPE"
        yield process.stdin, process.stdout

