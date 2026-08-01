
def ignore_suppressed_imports(module: str) -> bool:
    """Can we skip looking for newly unsuppressed imports to module?"""
    # Various submodules of 'encodings' can be suppressed, since it
    # uses module-level '__getattr__'. Skip them since there are many
    # of them, and following imports to them is kind of pointless.
    return module.startswith("encodings.")

