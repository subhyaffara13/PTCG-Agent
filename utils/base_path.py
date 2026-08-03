import os

def base_path(main_path, fmt, formats=None):
    """Given a path and options for a format (ext, suffix, prefix), return the corresponding base path"""
    fmt = long_form_one_format(fmt)

    base, ext = os.path.splitext(main_path)
    if "extension" not in fmt:
        fmt["extension"] = ext
        if ext not in NOTEBOOK_EXTENSIONS:
            raise NonNotebookExtension(
                "'{}' is not a notebook. Supported extensions are '{}'.".format(main_path, "', '".join(NOTEBOOK_EXTENSIONS))
            )

    if ext != fmt["extension"]:
        raise InconsistentExtension(
            "Notebook path '{}' was expected to have extension '{}'".format(main_path, fmt["extension"])
        )

    # Is there a format that matches the main path?
    if formats is None:
        formats = [fmt]

    for f in formats:
        if f["extension"] != fmt["extension"]:
            continue
        if "format_name" in fmt and "format_name" in f and f["format_name"] != fmt["format_name"]:
            continue
        # extend 'fmt' with the format information (prefix, suffix) from f
        fmt = {key: fmt.get(key, value) for key, value in f.items()}
        break

    suffix = fmt.get("suffix")
    prefix = fmt.get("prefix")

    if suffix:
        if not base.endswith(suffix):
            raise InconsistentSuffix(f"Notebook name '{base}' was expected to end with suffix '{suffix}'")
        base = base[: -len(suffix)]

    if not prefix:
        return base

    (
        prefix_root,
        prefix_dir,
        prefix_file_name,
    ) = get_prefix_root_prefix_dir_prefix_file_name(prefix)
    sep = separator(base)
    notebook_dir, notebook_file_name = split(base, sep)

    base_dir = None
    config_file = find_jupytext_configuration_file(notebook_dir)
    if config_file:
        config_file_dir = os.path.dirname(config_file)
        if notebook_dir.startswith(config_file_dir):
            base_dir = config_file_dir
            notebook_dir = notebook_dir[len(config_file_dir) :]

    if prefix_file_name:
        if not notebook_file_name.startswith(prefix_file_name):
            raise InconsistentPrefix(
                f"Notebook name '{notebook_file_name}' was expected to start with prefix '{prefix_file_name}'"
            )
        notebook_file_name = notebook_file_name[len(prefix_file_name) :]

    if prefix_dir:
        parent_notebook_dir = notebook_dir
        parent_prefix_dir = prefix_dir
        actual_folders = list()
        while parent_prefix_dir:
            parent_prefix_dir, expected_folder = split(parent_prefix_dir, "/")
            if expected_folder == "..":
                if not actual_folders:
                    raise InconsistentPrefixDirectory(
                        f"Notebook directory '{notebook_dir}' does not match prefix '{prefix_dir}'"
                    )
                parent_notebook_dir = join(parent_notebook_dir, actual_folders.pop(), sep)
            else:
                parent_notebook_dir, actual_folder = split(parent_notebook_dir, sep)
                actual_folders.append(actual_folder)

                if actual_folder != expected_folder:
                    raise InconsistentPrefixDirectory(
                        f"Notebook directory '{notebook_dir}' does not match prefix '{prefix_dir}'"
                    )
        notebook_dir = parent_notebook_dir

    if prefix_root:
        long_prefix_root = sep + prefix_root.replace("/", sep) + sep
        long_notebook_dir = sep + notebook_dir + sep
        if long_prefix_root not in long_notebook_dir:
            raise InconsistentPrefixRoot(f"Notebook directory '{notebook_dir}' does not match prefix root '{prefix_root}'")
        left, right = long_notebook_dir.rsplit(long_prefix_root, 1)
        notebook_dir = left + sep + "//" + right

        # We are going to remove the last char, but we need to insert it back in the end...
        if not right:
            sep = notebook_dir[-1]
        notebook_dir = notebook_dir[len(sep) : -len(sep)]

    if base_dir:
        notebook_dir = base_dir + notebook_dir

    if not notebook_dir:
        return notebook_file_name

    return notebook_dir + sep + notebook_file_name

