
def _pause_echo(stream: EchoingStdin | None) -> cabc.Generator[None]:
    if stream is None:
        yield
    else:
        stream._paused = True
        yield
        stream._paused = False

