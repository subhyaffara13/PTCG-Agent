from pathlib import Path


def temp_style(style_name, settings=None):
    """Context manager to create a style sheet in a temporary directory."""
    if not settings:
        settings = DUMMY_SETTINGS
    temp_file = f'{style_name}.mplstyle'
    orig_library_paths = style.USER_LIBRARY_PATHS
    try:
        with TemporaryDirectory() as tmpdir:
            # Write style settings to file in the tmpdir.
            Path(tmpdir, temp_file).write_text(
                "\n".join(f"{k}: {v}" for k, v in settings.items()),
                encoding="utf-8")
            # Add tmpdir to style path and reload so we can access this style.
            style.USER_LIBRARY_PATHS.append(tmpdir)
            style.reload_library()
            yield
    finally:
        style.USER_LIBRARY_PATHS = orig_library_paths
        style.reload_library()

