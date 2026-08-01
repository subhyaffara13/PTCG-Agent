
def _get_image_inclusion_command():
    man = LatexManager._get_cached_or_new()
    man._stdin_writeln(
        r"\includegraphics[interpolate=true]{%s}"
        # Don't mess with backslashes on Windows.
        % cbook._get_data_path("images/matplotlib.png").as_posix())
    try:
        man._expect_prompt()
        return r"\includegraphics"
    except LatexError:
        # Discard the broken manager.
        LatexManager._get_cached_or_new_impl.cache_clear()
        return r"\pgfimage"

