from typing import Any, Callable

def runner_with_spinner_message(message: str) -> Callable[..., None]:
    """Provide a subprocess_runner that shows a spinner message.

    Intended for use with for BuildBackendHookCaller. Thus, the runner has
    an API that matches what's expected by BuildBackendHookCaller.subprocess_runner.
    """

    def runner(
        cmd: list[str],
        cwd: str | None = None,
        extra_environ: Mapping[str, Any] | None = None,
    ) -> None:
        with open_spinner(message) as spinner:
            call_subprocess(
                cmd,
                command_desc=message,
                cwd=cwd,
                extra_environ=extra_environ,
                spinner=spinner,
            )

    return runner

