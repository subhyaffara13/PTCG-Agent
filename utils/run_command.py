import logging
import os
import subprocess
import sys
from typing import Dict, List

def run_command(command: List[str], env: Dict[str, str]) -> None:
    """Replace the current process with the specified command.

    Replaces the current process with the specified command and the variables from `env`
    added in the current environment variables.

    Parameters
    ----------
    command: List[str]
        The command and it's parameters
    env: Dict
        The additional environment variables

    Returns
    -------
    None
        This function does not return any value. It replaces the current process with the new one.

    """
    # copy the current environment variables and add the vales from
    # `env`
    cmd_env = os.environ.copy()
    cmd_env.update(env)

    if sys.platform == "win32":
        # execvpe on Windows returns control immediately
        # rather than once the command has finished.
        p = Popen(command, universal_newlines=True, bufsize=0, shell=False, env=cmd_env)
        _, _ = p.communicate()

        sys.exit(p.returncode)
    else:
        os.execvpe(command[0], args=command, env=cmd_env)


def run_command(
    info: ScriptInfo,
    host: str,
    port: int,
    reload: bool,
    debugger: bool,
    with_threads: bool,
    cert: ssl.SSLContext | tuple[str, str | None] | t.Literal["adhoc"] | None,
    extra_files: list[str] | None,
    exclude_patterns: list[str] | None,
) -> None:
    """Run a local development server.

    This server is for development purposes only. It does not provide
    the stability, security, or performance of production WSGI servers.

    The reloader and debugger are enabled by default with the '--debug'
    option.
    """
    try:
        app: WSGIApplication = info.load_app()  # pyright: ignore
    except Exception as e:
        if is_running_from_reloader():
            # When reloading, print out the error immediately, but raise
            # it later so the debugger or server can handle it.
            traceback.print_exc()
            err = e

            def app(
                environ: WSGIEnvironment, start_response: StartResponse
            ) -> cabc.Iterable[bytes]:
                raise err from None

        else:
            # When not reloading, raise the error immediately so the
            # command fails.
            raise e from None

    debug = get_debug_flag()

    if reload is None:
        reload = debug

    if debugger is None:
        debugger = debug

    show_server_banner(debug, info.app_import_path)

    run_simple(
        host,
        port,
        app,
        use_reloader=reload,
        use_debugger=debugger,
        threaded=with_threads,
        ssl_context=cert,
        extra_files=extra_files,
        exclude_patterns=exclude_patterns,
    )


def run_command(commands, args, cwd=None, verbose=False, hide_stderr=False, env=None):
    """Call the given command(s)."""
    assert isinstance(commands, list)
    process = None

    popen_kwargs = {}
    if sys.platform == "win32":
        # This hides the console window if pythonw.exe is used
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        popen_kwargs["startupinfo"] = startupinfo

    for command in commands:
        dispcmd = str([command, *args])
        try:
            # remember shell=False, so use git.cmd on windows, not just git
            process = subprocess.Popen(
                [command, *args],
                cwd=cwd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=(subprocess.PIPE if hide_stderr else None),
                **popen_kwargs,
            )
            break
        except OSError:
            e = sys.exc_info()[1]
            if e.errno == errno.ENOENT:
                continue
            if verbose:
                print(f"unable to run {dispcmd}")
                print(e)
            return None, None
    else:
        if verbose:
            print(f"unable to find command, tried {commands}")
        return None, None
    stdout = process.communicate()[0].strip().decode()
    if process.returncode != 0:
        if verbose:
            print(f"unable to run {dispcmd} (error)")
            print(f"stdout was {stdout}")
        return None, process.returncode
    return stdout, process.returncode


def run_command(command: list[str], return_stdout=False):
    """
    Runs `command` with `subprocess.check_output` and will potentially return the `stdout`. Will also properly capture
    if an error occurred while running `command`
    """
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        if return_stdout:
            if hasattr(output, "decode"):
                output = output.decode("utf-8")
            return output
    except subprocess.CalledProcessError as e:
        raise SubprocessCallException(
            f"Command `{' '.join(command)}` failed with the following error:\n\n{e.output.decode()}"
        ) from e


def run_command(*args, **kwargs):
    return run_command_inner(*args, **kwargs).stdout


def run_command(
    cmd: Sequence[str],
    *,
    capture_output: bool = False,
    suppress_output: bool = False,
    cwd: str | None = None,
) -> str | None:
  """Runs a shell command."""
  cmd_str = ' '.join(cmd)
  if not suppress_output:
    logging.debug('Running command: %s', cmd_str)

  try:
    if capture_output:
      return (
          subprocess.check_output(cmd, stderr=subprocess.STDOUT, cwd=cwd)
          .decode('utf-8')
          .strip()
      )
    elif suppress_output:
      # If suppressed, capture it so we can show it on failure.
      subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, check=True)
      return None
    else:
      subprocess.check_call(cmd, cwd=cwd)
      return None
  except subprocess.CalledProcessError as e:
    Console.print_error(
        f'Command failed with exit code {e.returncode}: {cmd_str}'
    )
    # Output captured stdout/stderr if available
    output = getattr(e, 'output', None) or getattr(e, 'stdout', None)
    if output:
      if isinstance(output, bytes):
        output = output.decode('utf-8')
      print(f'\n--- Command Output ---\n{output}\n----------------------\n')

    stderr = getattr(e, 'stderr', None)
    if stderr:
      if isinstance(stderr, bytes):
        stderr = stderr.decode('utf-8')
      print(f'\n--- Command Stderr ---\n{stderr}\n----------------------\n')
    raise

