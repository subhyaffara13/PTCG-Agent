
def extension_install(
    ctx: typer.Context,
    repo_id: Annotated[
        str,
        typer.Argument(help="GitHub extension repository in `[OWNER/]hf-<name>` format."),
    ],
    force: Annotated[bool, typer.Option("--force", help="Overwrite if already installed.")] = False,
) -> None:
    """Install an extension from a public GitHub repository.

    Security warning: this installs a third-party executable or Python package.
    Install only from sources you trust.
    """
    owner, repo_name, short_name = _normalize_repo_id(repo_id)
    root_ctx = ctx.find_root()
    reserved_commands = set(getattr(root_ctx.command, "commands", {}).keys())
    if short_name in reserved_commands:
        raise CLIError(
            f"Cannot install extension '{short_name}' because it conflicts with an existing `hf {short_name}` command."
        )

    extension_dir = _get_extension_dir(short_name)
    extension_exists = extension_dir.exists()
    if extension_exists and not force:
        raise CLIError(f"Extension '{short_name}' is already installed. Use --force to overwrite.")

    branch, description = _resolve_github_repo_info(owner=owner, repo_name=repo_name)

    if extension_exists:
        shutil.rmtree(extension_dir)

    manifest = _install_extension_from_github(
        owner=owner,
        repo_name=repo_name,
        short_name=short_name,
        extension_dir=extension_dir,
        branch=branch,
        description=description,
    )
    ext_type = manifest.type.capitalize()
    out.result(
        f"{ext_type} extension installed",
        source=f"{owner}/{repo_name}",
        command=f"hf {short_name}",
    )
    out.hint(f"Run it with: hf {short_name}")

