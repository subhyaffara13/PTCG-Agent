
def spawn(self, cmd, **kwargs) -> None:  # type: ignore[no-untyped-def]
    new_cmd = list(cmd)
    if PYODIDE:
        for argument in reversed(new_cmd):
            if not str(argument).endswith(".c"):
                continue
            if "base64/arch/" in str(argument):
                new_cmd.extend(["-msimd128"])
    elif not NO_EXTRA_FLAGS:
        compiler_type: str = self.compiler_type
        extra_options = EXTRA_FLAGS_PER_COMPILER_TYPE_PER_PATH_COMPONENT.get(compiler_type, None)
        if X86_64 and extra_options is not None:
            # filenames are closer to the end of command line
            for argument in reversed(new_cmd):
                # Check if the matching argument contains a source filename.
                if not str(argument).endswith(".c"):
                    continue

                for path in extra_options.keys():
                    if path in str(argument):
                        if compiler_type == "bcpp":
                            compiler = new_cmd.pop()
                            # Borland accepts a source file name at the end,
                            # insert the options before it
                            new_cmd.extend(extra_options[path])
                            new_cmd.append(compiler)
                        else:
                            new_cmd.extend(extra_options[path])

                        # path component is found, no need to search any further
                        break
    self.__spawn(new_cmd, **kwargs)


def spawn(fn, args=(), nprocs=1, join=True, daemon=False, start_method="spawn"):
    r"""Spawns ``nprocs`` processes that run ``fn`` with ``args``.

    If one of the processes exits with a non-zero exit status, the
    remaining processes are killed and an exception is raised with the
    cause of termination. In the case an exception was caught in the
    child process, it is forwarded and its traceback is included in
    the exception raised in the parent process.

    Args:
        fn (function): Function is called as the entrypoint of the
            spawned process. This function must be defined at the top
            level of a module so it can be pickled and spawned. This
            is a requirement imposed by multiprocessing.

            The function is called as ``fn(i, *args)``, where ``i`` is
            the process index and ``args`` is the passed through tuple
            of arguments.

        args (tuple): Arguments passed to ``fn``.
        nprocs (int): Number of processes to spawn.
        join (bool): Perform a blocking join on all processes.
        daemon (bool): The spawned processes' daemon flag. If set to True,
                       daemonic processes will be created.
        start_method (str): (deprecated) this method will always use ``spawn``
                               as the start method. To use a different start method
                               use ``start_processes()``.

    Returns:
        None if ``join`` is ``True``,
        :class:`~ProcessContext` if ``join`` is ``False``

    """
    if start_method != "spawn":
        msg = (
            f"This method only supports start_method=spawn (got: {start_method}).\n"
            "To use a different start_method use:\n\t\t"
            " torch.multiprocessing.start_processes(...)"
        )
        warnings.warn(msg, FutureWarning, stacklevel=2)
    return start_processes(fn, args, nprocs, join, daemon, start_method="spawn")


def spawn(
    cmd: MutableSequence[bytes | str | os.PathLike[str]],
    search_path: bool = True,
    verbose: bool = False,
    env: _ENV | None = None,
) -> None:
    """Run another program, specified as a command list 'cmd', in a new process.

    'cmd' is just the argument list for the new process, ie.
    cmd[0] is the program to run and cmd[1:] are the rest of its arguments.
    There is no way to run a program with a name different from that of its
    executable.

    If 'search_path' is true (the default), the system's executable
    search path will be used to find the program; otherwise, cmd[0]
    must be the exact path to the executable.

    Raise DistutilsExecError if running the program fails in any way; just
    return on success.
    """
    log.info(subprocess.list2cmdline(cmd))

    if search_path:
        executable = shutil.which(cmd[0])
        if executable is not None:
            cmd[0] = executable

    try:
        subprocess.check_call(cmd, env=_inject_macos_ver(env))
    except OSError as exc:
        raise DistutilsExecError(
            f"command {_debug(cmd)!r} failed: {exc.args[-1]}"
        ) from exc
    except subprocess.CalledProcessError as err:
        raise DistutilsExecError(
            f"command {_debug(cmd)!r} failed with exit code {err.returncode}"
        ) from err


def spawn(self, cmd, **kwargs) -> None:  # type: ignore[no-untyped-def]
    new_cmd = list(cmd)
    if PYODIDE:
        for argument in reversed(new_cmd):
            if not str(argument).endswith(".c"):
                continue
            if "base64/arch/" in str(argument):
                new_cmd.extend(["-msimd128"])
    elif not NO_EXTRA_FLAGS:
        compiler_type: str = self.compiler_type
        extra_options = EXTRA_FLAGS_PER_COMPILER_TYPE_PER_PATH_COMPONENT.get(compiler_type, None)
        if X86_64 and extra_options is not None:
            # filenames are closer to the end of command line
            for argument in reversed(new_cmd):
                # Check if the matching argument contains a source filename.
                if not str(argument).endswith(".c"):
                    continue

                for path in extra_options.keys():
                    if path in str(argument):
                        if compiler_type == "bcpp":
                            compiler = new_cmd.pop()
                            # Borland accepts a source file name at the end,
                            # insert the options before it
                            new_cmd.extend(extra_options[path])
                            new_cmd.append(compiler)
                        else:
                            new_cmd.extend(extra_options[path])

                        # path component is found, no need to search any further
                        break
    self.__spawn(new_cmd, **kwargs)

