import sys
from typing import Any

def importorskip(
    modname: str,
    minversion: str | None = None,
    reason: str | None = None,
    *,
    exc_type: type[ImportError] | None = None,
) -> Any:
    """Import and return the requested module ``modname``, or skip the
    current test if the module cannot be imported.

    :param modname:
        The name of the module to import.
    :param minversion:
        If given, the imported module's ``__version__`` attribute must be at
        least this minimal version, otherwise the test is still skipped.
    :param reason:
        If given, this reason is shown as the message when the module cannot
        be imported.
    :param exc_type:
        The exception that should be captured in order to skip modules.
        Must be :py:class:`ImportError` or a subclass.

        Defaults to :class:`ModuleNotFoundError` when not given, which means
        the module must be missing for the test to be skipped.
        Pass ``exc_type=ImportError`` to also skip modules that raise
        :class:`ImportError` during import.

        See :ref:`import-or-skip-import-error` for details.


    :returns:
        The imported module. This should be assigned to its canonical name.

    :raises pytest.skip.Exception:
        If the module cannot be imported.

    Example::

        docutils = pytest.importorskip("docutils")

    .. versionadded:: 8.2

        The ``exc_type`` parameter.

    .. versionchanged:: 9.1

        The default for ``exc_type`` is now :class:`ModuleNotFoundError`.
    """
    import warnings

    __tracebackhide__ = True
    compile(modname, "", "eval")  # to catch syntaxerrors

    # Keep the public signature compatible while using the pytest 9.1 default behavior.
    if exc_type is None:
        exc_type = ModuleNotFoundError

    skipped: Skipped | None = None

    with warnings.catch_warnings():
        # Make sure to ignore ImportWarnings that might happen because
        # of existing directories with the same name we're trying to
        # import but without a __init__.py file.
        warnings.simplefilter("ignore")

        try:
            importlib.import_module(modname)
        except exc_type as exc:
            # Do not raise or issue warnings inside the catch_warnings() block.
            if reason is None:
                reason = f"could not import {modname!r}: {exc}"
            skipped = Skipped(reason, allow_module_level=True)
    if skipped:
        raise skipped

    mod = sys.modules[modname]
    if minversion is None:
        return mod
    verattr = getattr(mod, "__version__", None)
    if minversion is not None:
        # Imported lazily to improve start-up time.
        from packaging.version import Version

        if verattr is None or Version(verattr) < Version(minversion):
            raise Skipped(
                f"module {modname!r} has __version__ {verattr!r}, required is: {minversion!r}",
                allow_module_level=True,
            )
    return mod

