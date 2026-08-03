import sys

def _prevent_further_imports() -> None:
    """Install an audit hook that warns on unexpected imports after pip install starts.

    Eagerly pre-imports the known lazy imports first so the hook only fires
    on genuinely unexpected modules.
    """
    global _IMPORT_AUDIT_HOOK_INSTALLED
    if _IMPORT_AUDIT_HOOK_INSTALLED:
        return

    _IMPORT_AUDIT_HOOK_INSTALLED = True
    sys.addaudithook(_prevent_import_hook)

