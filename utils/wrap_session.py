import os
import sys
from typing import Callable

def wrap_session(
    config: Config, doit: Callable[[Config, Session], int | ExitCode | None]
) -> int | ExitCode:
    """Skeleton command line program."""
    session = Session.from_config(config)
    session.exitstatus = ExitCode.OK
    initstate = 0
    try:
        try:
            config._do_configure()
            initstate = 1
            config.hook.pytest_sessionstart(session=session)
            initstate = 2
            session.exitstatus = doit(config, session) or 0
        except UsageError:
            session.exitstatus = ExitCode.USAGE_ERROR
            raise
        except Failed:
            session.exitstatus = ExitCode.TESTS_FAILED
        except (KeyboardInterrupt, exit.Exception):
            excinfo = _pytest._code.ExceptionInfo.from_current()
            exitstatus: int | ExitCode = ExitCode.INTERRUPTED
            if isinstance(excinfo.value, exit.Exception):
                if excinfo.value.returncode is not None:
                    exitstatus = excinfo.value.returncode
                if initstate < 2:
                    sys.stderr.write(f"{excinfo.typename}: {excinfo.value.msg}\n")
            config.hook.pytest_keyboard_interrupt(excinfo=excinfo)
            session.exitstatus = exitstatus
        except BaseException:
            session.exitstatus = ExitCode.INTERNAL_ERROR
            excinfo = _pytest._code.ExceptionInfo.from_current()
            try:
                config.notify_exception(excinfo, config.option)
            except exit.Exception as exc:
                if exc.returncode is not None:
                    session.exitstatus = exc.returncode
                sys.stderr.write(f"{type(exc).__name__}: {exc}\n")
            else:
                if isinstance(excinfo.value, SystemExit):
                    sys.stderr.write("mainloop: caught unexpected SystemExit!\n")

    finally:
        # Explicitly break reference cycle.
        excinfo = None  # type: ignore
        os.chdir(session.startpath)
        if initstate >= 2:
            try:
                config.hook.pytest_sessionfinish(
                    session=session, exitstatus=session.exitstatus
                )
            except exit.Exception as exc:
                if exc.returncode is not None:
                    session.exitstatus = exc.returncode
                sys.stderr.write(f"{type(exc).__name__}: {exc}\n")
        config._ensure_unconfigure()
    return session.exitstatus

