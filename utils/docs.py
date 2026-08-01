
def docs(session: nox.Session) -> None:
    """
    Build the docs. Pass "serve" to serve.
    """

    session.install("-r", "docs/requirements.txt")
    session.chdir("docs")

    if "pdf" in session.posargs:
        session.run("sphinx-build", "-M", "latexpdf", ".", "_build")
        return

    session.run("sphinx-build", "-M", "html", ".", "_build")

    if "serve" in session.posargs:
        session.log("Launching docs at http://localhost:8000/ - use Ctrl-C to quit")
        session.run("python", "-m", "http.server", "8000", "-d", "_build/html")
    elif session.posargs:
        session.error("Unsupported argument to docs")


def docs(
    ctx: typer.Context,
    name: str = typer.Option("", help="The name of the CLI program to use in docs."),
    output: Path | None = typer.Option(
        None,
        help="An output file to write docs to, like README.md.",
        file_okay=True,
        dir_okay=False,
    ),
    title: str | None = typer.Option(
        None,
        help="The title for the documentation page. If not provided, the name of "
        "the program is used.",
    ),
) -> None:
    """
    Generate Markdown docs for a Typer app.
    """
    typer_obj = get_typer_from_state()
    if not typer_obj:
        typer.echo("No Typer app found", err=True)
        raise typer.Abort()
    if hasattr(typer_obj, "rich_markup_mode"):
        if not hasattr(ctx, "obj") or ctx.obj is None:
            ctx.ensure_object(dict)
        if isinstance(ctx.obj, dict):
            ctx.obj[MARKUP_MODE_KEY] = typer_obj.rich_markup_mode
    click_obj = typer.main.get_command(typer_obj)
    docs = get_docs_for_click(obj=click_obj, ctx=ctx, name=name, title=title)
    clean_docs = f"{docs.strip()}\n"
    if output:
        output.write_text(clean_docs)
        typer.echo(f"Docs saved to: {output}")
    else:
        typer.echo(clean_docs)

