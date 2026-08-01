
def load_paired_notebook(
    notebook,
    fmt,
    config,
    formats,
    nb_file,
    log,
    pre_commit_mode: bool,
    timestamp_checker: TimestampChecker,
    read_func,
):
    """Update the notebook with the inputs and outputs of the most recent paired files"""
    if not formats:
        raise NotAPairedNotebook(f"{shlex.quote(nb_file)} is not a paired notebook")

    formats = long_form_multiple_formats(formats)
    _, fmt_with_prefix_suffix = find_base_path_and_format(nb_file, formats)
    fmt.update(fmt_with_prefix_suffix)

    def read_one_file(path, fmt):
        if path == nb_file:
            return notebook

        log(f"[jupytext] Loading {shlex.quote(path)}")
        timestamp_checker.get_and_check_timestamp(path)
        return read_func(path, fmt=fmt)

    if pre_commit_mode and file_in_git_index(nb_file):
        # We raise an error if two representations of this notebook in the git index are inconsistent
        nb_files_in_git_index = sorted(
            ((alt_path, alt_fmt) for alt_path, alt_fmt in paired_paths(nb_file, fmt, formats) if file_in_git_index(alt_path)),
            key=lambda x: 0 if x[1]["extension"] != ".ipynb" else 1,
        )

        if len(nb_files_in_git_index) > 1:
            path0, fmt0 = nb_files_in_git_index[0]
            timestamp_checker.get_and_check_timestamp(path0)
            with open(path0, encoding="utf-8") as fp:
                text0 = fp.read()
            for alt_path, alt_fmt in nb_files_in_git_index[1:]:
                timestamp_checker.get_and_check_timestamp(alt_path)
                nb = read(alt_path, fmt=alt_fmt, config=config)
                alt_text = writes(nb, fmt=fmt0, config=config)
                if alt_text != text0:
                    diff = compare(alt_text, text0, alt_path, path0, return_diff=True)
                    raise InconsistentVersions(
                        f"{shlex.quote(alt_path)} and {shlex.quote(path0)} are inconsistent.\n"
                        + diff
                        + f"\nPlease revert JUST ONE of the files with EITHER\n"
                        f"    git reset {shlex.quote(alt_path)} && git checkout -- {shlex.quote(alt_path)}\nOR\n"
                        f"    git reset {shlex.quote(path0)} && git checkout -- {shlex.quote(path0)}\n"
                    )

    inputs, outputs = latest_inputs_and_outputs(nb_file, fmt, formats, timestamp_checker.get_and_check_timestamp)
    notebook = read_pair(inputs, outputs, read_one_file)

    return notebook, inputs.path, outputs.path

