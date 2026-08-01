
def pipe_output(output: str) -> None:
    """Pipes output to a pager if stdout is a TTY and a pager is available."""

    if not output:
        return

    if not sys.stdout.isatty():
        sys.stdout.write(output)
        return

    pager = os.getenv("PAGER") or shutil.which("less")

    if not pager:
        sys.stdout.write(output)
        return

    pager_cmd = [pager]
    if "less" in os.path.basename(pager):
        pager_cmd.append("-R")

    proc = subprocess.Popen(pager_cmd, stdin=subprocess.PIPE, text=True)
    try:
        proc.stdin.write(output)
        proc.stdin.close()
        proc.wait()
    except (BrokenPipeError, KeyboardInterrupt):
        # Pager process was terminated before all output was written.
        # This is not an error. The main exception handler will deal with it.
        if proc.stdin:
            proc.stdin.close()
        # The process might still be running, but we have closed our side of the
        # pipe. The Popen destructor will send a SIGKILL to the child.
    except Exception:
        if proc.stdin:
            proc.stdin.close()
        raise

