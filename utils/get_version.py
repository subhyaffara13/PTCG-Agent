
def get_version(ctx: click.Context, param: click.Parameter, value: t.Any) -> None:
    if not value or ctx.resilient_parsing:
        return

    flask_version = importlib.metadata.version("flask")
    werkzeug_version = importlib.metadata.version("werkzeug")

    click.echo(
        f"Python {platform.python_version()}\n"
        f"Flask {flask_version}\n"
        f"Werkzeug {werkzeug_version}",
        color=ctx.color,
    )
    ctx.exit()


def get_version(nb):
    """Get the version of a notebook.

    Parameters
    ----------
    nb : dict
        NotebookNode or dict containing notebook data.

    Returns
    -------
    Tuple containing major (int) and minor (int) version numbers
    """
    major = nb.get("nbformat", 1)
    minor = nb.get("nbformat_minor", 0)
    return (major, minor)


def get_version(module: types.ModuleType) -> str:
    version = getattr(module, "__version__", None)

    if version is None:
        raise ImportError(f"Can't determine version for {module.__name__}")
    if module.__name__ == "psycopg2":
        # psycopg2 appends " (dt dec pq3 ext lo64)" to it's version
        version = version.split()[0]
    return version

