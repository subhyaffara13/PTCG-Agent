
def wrap_exceptions(fun):
    """Call callable into a try/except clause and translate ENOENT,
    EACCES and EPERM in NoSuchProcess or AccessDenied exceptions.
    """

    @functools.wraps(fun)
    def wrapper(self, *args, **kwargs):
        pid, ppid, name = self.pid, self._ppid, self._name
        try:
            return fun(self, *args, **kwargs)
        except (FileNotFoundError, ProcessLookupError) as err:
            # ENOENT (no such file or directory) gets raised on open().
            # ESRCH (no such process) can get raised on read() if
            # process is gone in meantime.
            if not pid_exists(pid):
                raise NoSuchProcess(pid, name) from err
            raise ZombieProcess(pid, name, ppid) from err
        except PermissionError as err:
            raise AccessDenied(pid, name) from err

    return wrapper


def wrap_exceptions(fun):
    """Decorator which translates bare OSError exceptions into
    NoSuchProcess and AccessDenied.
    """

    @functools.wraps(fun)
    def wrapper(self, *args, **kwargs):
        pid, ppid, name = self.pid, self._ppid, self._name
        try:
            return fun(self, *args, **kwargs)
        except ProcessLookupError as err:
            if cext.proc_is_zombie(pid):
                raise ZombieProcess(pid, name, ppid) from err
            raise NoSuchProcess(pid, name) from err
        except PermissionError as err:
            raise AccessDenied(pid, name) from err
        except cext.ZombieProcessError as err:
            raise ZombieProcess(pid, name, ppid) from err
        except OSError as err:
            if pid == 0 and 0 in pids():
                raise AccessDenied(pid, name) from err
            raise err from None

    return wrapper


def wrap_exceptions(fun):
    """Decorator which translates bare OSError exceptions into
    NoSuchProcess and AccessDenied.
    """

    @functools.wraps(fun)
    def wrapper(self, *args, **kwargs):
        pid, name = self.pid, self._name
        try:
            return fun(self, *args, **kwargs)
        except PermissionError as err:
            raise AccessDenied(pid, name) from err
        except ProcessLookupError as err:
            self._raise_if_zombie()
            raise NoSuchProcess(pid, name) from err
        except FileNotFoundError as err:
            self._raise_if_zombie()
            # /proc/PID directory may still exist, but the files within
            # it may not, indicating the process is gone, see:
            # https://github.com/giampaolo/psutil/issues/2418
            if not os.path.exists(f"{self._procfs_path}/{pid}/stat"):
                raise NoSuchProcess(pid, name) from err
            raise

    return wrapper


def wrap_exceptions(fun):
    """Decorator which translates bare OSError exceptions into
    NoSuchProcess and AccessDenied.
    """

    @functools.wraps(fun)
    def wrapper(self, *args, **kwargs):
        pid, ppid, name = self.pid, self._ppid, self._name
        try:
            return fun(self, *args, **kwargs)
        except ProcessLookupError as err:
            if cext.proc_is_zombie(pid):
                raise ZombieProcess(pid, name, ppid) from err
            raise NoSuchProcess(pid, name) from err
        except PermissionError as err:
            raise AccessDenied(pid, name) from err
        except cext.ZombieProcessError as err:
            raise ZombieProcess(pid, name, ppid) from err

    return wrapper


def wrap_exceptions(fun):
    """Call callable into a try/except clause and translate ENOENT,
    EACCES and EPERM in NoSuchProcess or AccessDenied exceptions.
    """

    @functools.wraps(fun)
    def wrapper(self, *args, **kwargs):
        pid, ppid, name = self.pid, self._ppid, self._name
        try:
            return fun(self, *args, **kwargs)
        except (FileNotFoundError, ProcessLookupError) as err:
            # ENOENT (no such file or directory) gets raised on open().
            # ESRCH (no such process) can get raised on read() if
            # process is gone in meantime.
            if not pid_exists(pid):
                raise NoSuchProcess(pid, name) from err
            raise ZombieProcess(pid, name, ppid) from err
        except PermissionError as err:
            raise AccessDenied(pid, name) from err
        except OSError as err:
            if pid == 0:
                if 0 in pids():
                    raise AccessDenied(pid, name) from err
                raise
            raise

    return wrapper


def wrap_exceptions(fun):
    """Decorator which converts OSError into NoSuchProcess or AccessDenied."""

    @functools.wraps(fun)
    def wrapper(self, *args, **kwargs):
        try:
            return fun(self, *args, **kwargs)
        except OSError as err:
            raise convert_oserror(err, pid=self.pid, name=self._name) from err

    return wrapper


def wrap_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OSError as exception:
            if not exception.args:
                raise

            message, *args = exception.args
            if isinstance(message, str) and "does not exist" in message:
                raise FileNotFoundError(errno.ENOENT, message) from exception
            else:
                raise

    return wrapper

