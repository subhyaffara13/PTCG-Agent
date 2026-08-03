import os
from pathlib import Path


def spaces_hot_reload(
    space_id: Annotated[
        str,
        typer.Argument(
            help="The space ID (e.g. `username/repo-name`).",
        ),
    ],
    filename: Annotated[
        str | None,
        typer.Argument(
            help="Path to the Python file in the Space repository. Can be omitted when --local-file is specified and path in repository matches."
        ),
    ] = None,
    local_file: Annotated[
        Path | None,
        typer.Option(
            "--local-file",
            "-f",
            help="Path of local file. Interactive editor mode if not specified",
        ),
    ] = None,
    skip_checks: Annotated[bool, typer.Option(help="Skip hot-reload compatibility checks.")] = False,
    skip_summary: Annotated[bool, typer.Option(help="Skip summary display after hot-reload is triggered")] = False,
    token: TokenOpt = None,
) -> None:
    """
    Hot-reload any Python file of a Space without a full rebuild + restart.

    ⚠ This feature is experimental ⚠

    Only works with Gradio SDK (6.1+)
    Opens an interactive editor unless --local-file/-f is specified.

    This command patches the live Python process using https://github.com/breuleux/jurigged
    (AST-based diffing, in-place function updates, etc.), integrated with Gradio's native hot-reload support
    (meaning that Gradio demo object changes are reflected in the UI)

    The command creates a remote commit.
    If you are working from a local clone, run `git pull --autostash` afterwards
    to bring the commit back and keep your local git state in sync.
    """

    typer.secho("This feature is experimental and subject to change", fg=typer.colors.BRIGHT_BLACK)

    api = get_hf_api(token=token)

    if not skip_checks:
        space_info = api.space_info(space_id)
        if space_info.sdk != "gradio":
            raise CLIError(f"Hot-reloading is only available on Gradio SDK. Found {space_info.sdk} SDK")
        if (card_data := space_info.card_data) is None:
            raise CLIError(f"Unable to read cardData for Space {space_id}")
        if (sdk_version := card_data.sdk_version) is None:
            raise CLIError(f"Unable to read sdk_version from {space_id} cardData")
        if version.parse(sdk_version) < version.Version(HOT_RELOADING_MIN_GRADIO):
            raise CLIError(f"Hot-reloading requires Gradio >= {HOT_RELOADING_MIN_GRADIO} (found {sdk_version})")
        if (current_sha := space_info.sha) is None:
            raise CLIError(f"Unexpected `None` running SHA for Space {space_id}")
    else:
        current_sha = None

    if local_file:
        local_path = str(local_file)
        filename = local_file.as_posix() if filename is None else filename
    elif filename:
        if not skip_checks:
            try:
                api.auth_check(
                    repo_type="space",
                    repo_id=space_id,
                    write=True,
                )
            except RepositoryNotFoundError as e:
                raise CLIError(
                    f"Write access check to {space_id} repository failed. Make sure that you are authenticated"
                ) from e
        temp_dir = tempfile.TemporaryDirectory()
        local_path = os.path.join(temp_dir.name, filename)
        with disable_progress_bars():
            try:
                hf_hub_download(repo_type="space", repo_id=space_id, filename=filename, local_dir=temp_dir.name)
            except RemoteEntryNotFoundError:
                typer.secho(
                    f"{filename} not found in remote repository. Assuming new file", fg=typer.colors.BRIGHT_BLACK
                )

        editor_res = _editor_open(local_path)
        if editor_res == "no-tty":
            persistent_temp_dir = tempfile.mkdtemp()
            shutil.copytree(temp_dir.name, persistent_temp_dir, dirs_exist_ok=True)
            local_path = os.path.join(persistent_temp_dir, filename)
            typer.secho("No TTY detected. Non-interactive fallback:")
            typer.secho(f"- Edit {local_path}")
            typer.secho(f"- Run `hf spaces hot-reload {space_id} {filename} -f {local_path}`")
            return
        if editor_res == "no-editor":
            raise CLIError("No editor found in local environment. Use -f flag to hot-reload from local path")
        if editor_res != 0:
            raise CLIError(f"Editor returned a non-zero exit code while attempting to edit {local_path}")
    else:
        raise CLIError("Either filename or --local-file/-f must be specified")

    commit_info = api.upload_file(
        repo_type="space",
        repo_id=space_id,
        path_or_fileobj=local_path,
        path_in_repo=filename,
        parent_commit=current_sha,
        _hot_reload=True,
    )

    if local_file is not None and local_file.resolve().is_relative_to(Path.cwd()):
        typer.secho(f"Created commit {commit_info.oid} in remote Space repository.")
        typer.secho("Consider running `git pull --autostash` to stay synced if you are working from a local clone.")

    if not skip_summary:
        typer.secho("Hot-reload summary:")
        _spaces_hot_reload_summary(
            api=api,
            space_id=space_id,
            current_sha=current_sha,
            commit_sha=commit_info.oid,
            local_path=local_path if local_file else filename,
            filename=filename,
            token=token,
        )

