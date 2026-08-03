import re

def guess_format(text, ext):
    """Guess the format and format options of the file, given its extension and content"""
    metadata = read_metadata(text, ext)

    if "text_representation" in metadata.get("jupytext", {}):
        return format_name_for_ext(metadata, ext), {}

    if is_myst_available() and ext in myst_extensions() and matches_mystnb(text, ext, requires_meta=False):
        return MYST_FORMAT_NAME, {}

    lines = text.splitlines()

    # Is this a Hydrogen-like script?
    # Or a Sphinx-gallery script?
    if ext in _SCRIPT_EXTENSIONS:
        unescaped_comment = _SCRIPT_EXTENSIONS[ext]["comment"]
        comment = re.escape(unescaped_comment)
        language = _SCRIPT_EXTENSIONS[ext]["language"]
        twenty_hash_re = re.compile(r"^#( |)#{19,}\s*$")
        double_percent_re = re.compile(rf"^{comment}( %%|%%)$")
        double_percent_and_space_re = re.compile(rf"^{comment}( %%|%%)\s")
        nbconvert_script_re = re.compile(rf"^{comment}( <codecell>| In\[[0-9 ]*\]:?)")
        vim_folding_markers_re = re.compile(rf"^{comment}\s*" + "{{{")
        vscode_folding_markers_re = re.compile(rf"^{comment}\s*region")
        marimo_cell_re = re.compile(r"^@app.cell.*")

        twenty_hash_count = 0
        double_percent_count = 0
        magic_command_count = 0
        rspin_comment_count = 0
        vim_folding_markers_count = 0
        vscode_folding_markers_count = 0
        marimo_app_count = 0

        parser = StringParser(language="R" if ext in [".r", ".R"] else "python")
        for line in lines:
            parser.read_line(line)
            if parser.is_quoted():
                continue

            # Don't count escaped Jupyter magics (no space between %% and command) as cells
            if double_percent_re.match(line) or double_percent_and_space_re.match(line) or nbconvert_script_re.match(line):
                double_percent_count += 1

            if not line.startswith(unescaped_comment) and is_magic(line, language):
                magic_command_count += 1

            if twenty_hash_re.match(line) and ext == ".py":
                twenty_hash_count += 1

            if line.startswith("#'") and ext in [".R", ".r"]:
                rspin_comment_count += 1

            if vim_folding_markers_re.match(line):
                vim_folding_markers_count += 1

            if vscode_folding_markers_re.match(line):
                vscode_folding_markers_count += 1

            if ext == ".py" and (line in {"import marimo", "app = marimo.App()"} or marimo_cell_re.match(line)):
                marimo_app_count += 1

        if double_percent_count >= 1:
            if magic_command_count:
                return "hydrogen", {}
            return "percent", {}

        if marimo_app_count >= 2:
            return "marimo", {}

        if vim_folding_markers_count:
            return "light", {"cell_markers": "{{{,}}}"}

        if vscode_folding_markers_count:
            return "light", {"cell_markers": "region,endregion"}

        if twenty_hash_count >= 2:
            return "sphinx", {}

        if rspin_comment_count >= 1:
            return "spin", {}

    if ext in [".md", ".markdown"]:
        for line in lines:
            if line.startswith(":::"):  # Pandoc div
                return "pandoc", {}

    # Default format
    return get_format_implementation(ext).format_name, {}

