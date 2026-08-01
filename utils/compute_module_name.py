
def compute_module_name(root: Path, module_path: Path) -> str | None:
    """Compute a module name based on a path and a root anchor."""
    try:
        path_without_suffix = module_path.with_suffix("")
    except ValueError:
        # Empty paths (such as Path.cwd()) might break meta_path hooks (like our own assertion rewriter).
        return None

    try:
        relative = path_without_suffix.relative_to(root)
    except ValueError:  # pragma: no cover
        return None
    names = list(relative.parts)
    if not names:
        return None
    if names[-1] == "__init__":
        names.pop()
    return ".".join(names)

