
def exec_ssh(
    destination: str, *, port: int | None = None, identity_file: Path | None = None, dry_run: bool = False
) -> None:
    """Run an interactive `ssh` command to `destination` (`user@host`) and exit with its return code.

    With `dry_run`, print the command instead of running it.
    """
    cmd = ["ssh"]
    if identity_file is not None:
        cmd += ["-i", str(identity_file)]
    if port is not None:
        cmd += ["-p", str(port)]
    cmd.append(destination)
    if dry_run:
        out.text(shlex.join(cmd))
        return
    out.text(f"Running `{shlex.join(cmd)}`")
    result = subprocess.run(cmd)
    raise typer.Exit(code=result.returncode)

