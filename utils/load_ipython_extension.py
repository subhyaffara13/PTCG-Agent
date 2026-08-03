from typing import Any

def load_ipython_extension(ipython):
    """Register the %dotenv magic."""
    ipython.register_magics(IPythonDotEnv)


def load_ipython_extension(ipython: Any) -> None:
    from .ipython import load_ipython_extension

    load_ipython_extension(ipython)


def load_ipython_extension(ip: Any) -> None:  # pragma: no cover
    # prevent circular import
    from rich.pretty import install
    from rich.traceback import install as tr_install

    install()
    tr_install()


def load_ipython_extension(ip: Any) -> None:  # pragma: no cover
    # prevent circular import
    from pip._vendor.rich.pretty import install
    from pip._vendor.rich.traceback import install as tr_install

    install()
    tr_install()

