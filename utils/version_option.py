
def version_option(
    version: str | None = None,
    *param_decls: str,
    package_name: str | None = None,
    prog_name: str | None = None,
    message: str | None = None,
    **kwargs: t.Any,
) -> t.Callable[[FC], FC]:
    """Add a ``--version`` option which immediately prints the version
    number and exits the program.

    If ``version`` is not provided, Click will try to detect it using
    :func:`importlib.metadata.version` to get the version for the
    ``package_name``.

    If ``package_name`` is not provided, Click will try to detect it by
    inspecting the stack frames. If the detected (or given) name does
    not match an installed distribution, Click resolves it as an import
    (top-level module) name via
    :func:`importlib.metadata.packages_distributions`, so e.g. ``PIL``
    resolves to the ``Pillow`` distribution.

    :param version: The version number to show. If not provided, Click
        will try to detect it.
    :param param_decls: One or more option names. Defaults to the single
        value ``"--version"``.
    :param package_name: The package name to detect the version from. If
        not provided, Click will try to detect it.
    :param prog_name: The name of the CLI to show in the message. If not
        provided, it will be detected from the command.
    :param message: The message to show. The values ``%(prog)s``,
        ``%(package)s``, and ``%(version)s`` are available. Defaults to
        ``"%(prog)s, version %(version)s"``.
    :param kwargs: Extra arguments are passed to :func:`option`.
    :raise RuntimeError: ``version`` could not be detected.

    .. versionchanged:: 8.0
        Add the ``package_name`` parameter, and the ``%(package)s``
        value for messages.

    .. versionchanged:: 8.0
        Use :mod:`importlib.metadata` instead of ``pkg_resources``. The
        version is detected based on the package name, not the entry
        point name. The Python package name must match the installed
        package name, or be passed with ``package_name=``.

    .. versionchanged:: 8.4.2
        When ``package_name`` does not match an installed distribution,
        Click now resolves it as an import (top-level module).
    """
    if message is None:
        message = _("%(prog)s, version %(version)s")

    if version is None and package_name is None:
        frame = inspect.currentframe()
        f_back = frame.f_back if frame is not None else None
        f_globals = f_back.f_globals if f_back is not None else None
        # break reference cycle
        # https://docs.python.org/3/library/inspect.html#the-interpreter-stack
        del frame

        if f_globals is not None:
            package_name = f_globals.get("__name__")

            if package_name == "__main__":
                package_name = f_globals.get("__package__")

            if package_name:
                package_name = package_name.partition(".")[0]

    def callback(ctx: Context, param: Parameter, value: bool) -> None:
        if not value or ctx.resilient_parsing:
            return

        nonlocal prog_name
        nonlocal version
        nonlocal package_name

        if prog_name is None:
            prog_name = ctx.find_root().info_name

        if version is None and package_name is not None:
            import importlib.metadata

            try:
                version = importlib.metadata.version(package_name)
            except importlib.metadata.PackageNotFoundError:
                # The given name didn't match an installed distribution.
                # Try resolving it as an import (top-level module) name,
                # e.g. ``PIL`` is provided by the ``Pillow`` distribution.
                distributions = importlib.metadata.packages_distributions().get(
                    package_name, []
                )
                if len(distributions) == 1:
                    package_name = distributions[0]
                    version = importlib.metadata.version(package_name)
                elif len(distributions) > 1:
                    raise RuntimeError(
                        f"{package_name!r} maps to multiple installed"
                        f" distributions ({', '.join(distributions)})."
                        " Pass 'package_name' to disambiguate."
                    ) from None
                else:
                    raise RuntimeError(
                        f"{package_name!r} is not installed. Try passing"
                        " 'package_name' instead."
                    ) from None

        if version is None:
            raise RuntimeError(
                f"Could not determine the version for {package_name!r} automatically."
            )

        echo(
            message % {"prog": prog_name, "package": package_name, "version": version},
            color=ctx.color,
        )
        ctx.exit()

    if not param_decls:
        param_decls = ("--version",)

    kwargs.setdefault("is_flag", True)
    kwargs.setdefault("expose_value", False)
    kwargs.setdefault("is_eager", True)
    kwargs.setdefault("help", _("Show the version and exit."))
    kwargs["callback"] = callback
    return option(*param_decls, **kwargs)

