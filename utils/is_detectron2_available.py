
def is_detectron2_available() -> bool:
    # We need this try/except block because otherwise after uninstalling the library, it stays available for some reason
    # i.e. `import detectron2` and `import detectron2.modeling` still work, even though the library is uninstalled
    # (the package exists but the objects are not reachable) - so here we explicitly try to import an object from it
    try:
        from detectron2.modeling import META_ARCH_REGISTRY  # noqa

        return True
    except Exception:
        return False

