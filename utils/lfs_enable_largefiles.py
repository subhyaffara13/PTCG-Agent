
def lfs_enable_largefiles(
    path: Annotated[
        str,
        typer.Argument(
            help="Local path to repository you want to configure.",
        ),
    ],
) -> None:
    """
    Configure your repository to enable upload of files > 5GB.

    This command sets up git-lfs to use the custom multipart transfer agent
    which enables efficient uploading of large files in chunks.
    """
    local_path = os.path.abspath(path)
    if not os.path.isdir(local_path):
        raise CLIError("This does not look like a valid git repo.")
    subprocess.run(
        "git config lfs.customtransfer.multipart.path hf".split(),
        check=True,
        cwd=local_path,
    )
    subprocess.run(
        f"git config lfs.customtransfer.multipart.args {LFS_MULTIPART_UPLOAD_COMMAND}".split(),
        check=True,
        cwd=local_path,
    )
    out.result("Local repo set up for largefiles", path=local_path)

