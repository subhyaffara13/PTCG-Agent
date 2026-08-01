
def exec_command(command, input=None, capture=False, warn_only=False, quiet=False):
    """Execute the desired command, and pipe the given input into it"""
    assert isinstance(command, list)
    if not quiet:
        sys.stdout.write("[jupytext] Executing {}\n".format(" ".join(command)))
    process = subprocess.Popen(
        command,
        **(dict(stdout=subprocess.PIPE, stdin=subprocess.PIPE) if input is not None else {}),
    )
    out, err = process.communicate(input=input)
    if out and not capture and not quiet:
        sys.stdout.write(out.decode("utf-8"))
    if err:
        sys.stderr.write(err.decode("utf-8"))

    if process.returncode:
        msg = f"The command '{' '.join(command)}' exited with code {process.returncode}"
        hint = "" if warn_only else " (use --warn-only to turn this error into a warning)"
        sys.stderr.write(f"[jupytext] {'Warning' if warn_only else 'Error'}: {msg}{hint}\n")
        if not warn_only:
            raise SystemExit(process.returncode)

    return out

