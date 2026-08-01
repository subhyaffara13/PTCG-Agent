
def get_completion_class(shell: t.Literal["bash"]) -> type[BashComplete]: ...


def get_completion_class(shell: t.Literal["fish"]) -> type[FishComplete]: ...


def get_completion_class(shell: t.Literal["zsh"]) -> type[ZshComplete]: ...


def get_completion_class(shell: str) -> type[ShellComplete] | None: ...


def get_completion_class(shell: str) -> type[ShellComplete] | None:
    """Look up a registered :class:`ShellComplete` subclass by the name
    provided by the completion instruction environment variable. If the
    name isn't registered, returns ``None``.

    :param shell: Name the class is registered under.
    """
    return _available_shells.get(shell)

