
def full_path(base, fmt):
    """Return the full path for the notebook, given the base path"""
    ext = fmt["extension"]
    suffix = fmt.get("suffix")
    prefix = fmt.get("prefix")

    full = base

    if prefix:
        if "//" in prefix:
            prefix_root, prefix = prefix.rsplit("//", 1)
        else:
            prefix_root = ""
        prefix_dir, prefix_file_name = split(prefix, "/")

        # Local path separator (\\ on windows)
        sep = separator(base)
        prefix_dir = prefix_dir.replace("/", sep)

        if (prefix_root != "") != ("//" in base):
            raise InconsistentPath(
                "Notebook base name '{}' is not compatible with fmt={}. Make sure you use prefix roots "
                "in either none, or all of the paired formats".format(base, short_form_one_format(fmt))
            )
        if prefix_root:
            left, right = base.rsplit("//", 1)
            right_dir, notebook_file_name = split(right, sep)
            notebook_dir = left + prefix_root + sep + right_dir
        else:
            notebook_dir, notebook_file_name = split(base, sep)

        if prefix_file_name:
            notebook_file_name = prefix_file_name + notebook_file_name

        if prefix_dir:
            dotdot = ".." + sep
            while prefix_dir.startswith(dotdot):
                prefix_dir = prefix_dir[len(dotdot) :]
                notebook_dir = split(notebook_dir, sep)[0]

            # Do not add a path separator when notebook_dir is '/'
            if notebook_dir and not notebook_dir.endswith(sep):
                notebook_dir = notebook_dir + sep

            notebook_dir = notebook_dir + prefix_dir

        if notebook_dir and not notebook_dir.endswith(sep):
            notebook_dir = notebook_dir + sep

        full = notebook_dir + notebook_file_name

    if suffix:
        full = full + suffix

    return full + ext

