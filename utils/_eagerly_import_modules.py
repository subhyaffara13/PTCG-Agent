
def _eagerly_import_modules() -> None:
    """Import modules pip uses lazily so the audit hook ignores them later."""
    for module in _EAGER_IMPORTS:
        try:
            __import__(module)
        except ImportError:
            # Record the module as missing so the hook can raise ImportError
            # instead of trying to import it again.
            _MISSING_MODULES.add(module)

