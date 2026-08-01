
def run_commands(dist):
    """Given a Distribution object run all the commands,
    raising ``SystemExit`` errors in the case of failure.

    This function assumes that either ``sys.argv`` or ``dist.script_args``
    is already set accordingly.
    """
    try:
        dist.run_commands()
    except KeyboardInterrupt:
        raise SystemExit("interrupted")
    except OSError as exc:
        if DEBUG:
            sys.stderr.write(f"error: {exc}\n")
            raise
        else:
            raise SystemExit(f"error: {exc}")

    except (DistutilsError, CCompilerError) as msg:
        if DEBUG:
            raise
        else:
            raise SystemExit("error: " + str(msg))

    return dist

