
def process_package_roots(
    fscache: FileSystemCache | None, parser: argparse.ArgumentParser, options: Options
) -> None:
    """Validate and normalize package_root."""
    if fscache is None:
        parser.error("--package-root does not work here (no fscache)")
    assert fscache is not None  # Since mypy doesn't know parser.error() raises.
    # Do some stuff with drive letters to make Windows happy (esp. tests).
    current_drive, _ = os.path.splitdrive(os.getcwd())
    dot = os.curdir
    dotslash = os.curdir + os.sep
    dotdotslash = os.pardir + os.sep
    trivial_paths = {dot, dotslash}
    package_root = []
    for root in options.package_root:
        if os.path.isabs(root):
            parser.error(f"Package root cannot be absolute: {root!r}")
        drive, root = os.path.splitdrive(root)
        if drive and drive != current_drive:
            parser.error(f"Package root must be on current drive: {drive + root!r}")
        # Empty package root is always okay.
        if root:
            root = os.path.relpath(root)  # Normalize the heck out of it.
            if not root.endswith(os.sep):
                root = root + os.sep
            if root.startswith(dotdotslash):
                parser.error(f"Package root cannot be above current directory: {root!r}")
            if root in trivial_paths:
                root = ""
        package_root.append(root)
    options.package_root = package_root
    # Pass the package root on the filesystem cache.
    fscache.set_package_root(package_root)

