from typing import Callable

def _typer_param_setup_autocompletion_compat(
    self: click.Parameter,
    *,
    autocompletion: Callable[
        [click.Context, list[str], str], list[tuple[str, str] | str]
    ]
    | None = None,
) -> None:
    if self._custom_shell_complete is not None:
        import warnings

        warnings.warn(
            "In Typer, only the parameter 'autocompletion' is supported. "
            "The support for 'shell_complete' is deprecated and will be removed in upcoming versions. ",
            DeprecationWarning,
            stacklevel=2,
        )

    if autocompletion is not None:

        def compat_autocompletion(
            ctx: click.Context, param: click.core.Parameter, incomplete: str
        ) -> list["click.shell_completion.CompletionItem"]:
            from click.shell_completion import CompletionItem

            out = []

            for c in autocompletion(ctx, [], incomplete):
                if isinstance(c, tuple):
                    use_completion = CompletionItem(c[0], help=c[1])
                else:
                    assert isinstance(c, str)
                    use_completion = CompletionItem(c)

                if use_completion.value.startswith(incomplete):
                    out.append(use_completion)

            return out

        self._custom_shell_complete = compat_autocompletion

