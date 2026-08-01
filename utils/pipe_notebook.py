
def pipe_notebook(
    notebook,
    command,
    fmt="py:percent",
    update=True,
    quiet=False,
    prefix=None,
    directory=None,
    warn_only=False,
):
    """Pipe the notebook, in the desired representation, to the given command. Update the notebook
    with the returned content if desired."""
    if command in ["black", "flake8", "autopep8"]:
        command = command + " -"
    elif command in ["pytest", "unittest"]:
        command = command + " {}"

    fmt = long_form_one_format(fmt, notebook.metadata, auto_ext_requires_language_info=False)
    fmt = check_auto_ext(fmt, notebook.metadata, "--pipe-fmt")
    text = writes(notebook, fmt)

    command = shlex.split(command)
    if "{}" in command:
        if prefix is not None:
            prefix = prefix + "-"
        tmp_file_args = dict(
            mode="w+",
            encoding="utf8",
            prefix=prefix,
            suffix=fmt["extension"],
            dir=directory,
            delete=False,
        )
        try:
            tmp = NamedTemporaryFile(**tmp_file_args)
        except TypeError:
            # NamedTemporaryFile does not have an 'encoding' argument on pypy
            tmp_file_args.pop("encoding")
            tmp = NamedTemporaryFile(**tmp_file_args)
        try:
            tmp.write(text)
            tmp.close()

            exec_command(
                [cmd if cmd != "{}" else tmp.name for cmd in command],
                capture=update,
                quiet=quiet,
                warn_only=warn_only,
            )

            if not update:
                return notebook

            piped_notebook = read(tmp.name, fmt=fmt)
        finally:
            os.remove(tmp.name)
    else:
        cmd_output = exec_command(
            command,
            text.encode("utf-8"),
            capture=update,
            warn_only=warn_only,
            quiet=quiet,
        )

        if not update:
            return notebook

        if not cmd_output:
            sys.stderr.write(
                "[jupytext] The command '{}' had no output. As a result, the notebook is empty. "
                "Is this expected? If not, use --check rather than --pipe for this command.".format(command)
            )

        piped_notebook = reads(cmd_output.decode("utf-8"), fmt)

    if fmt["extension"] != ".ipynb":
        piped_notebook = combine_inputs_with_outputs(piped_notebook, notebook, fmt)

    # Remove jupytext / text_representation entry
    if "jupytext" in notebook.metadata:
        piped_notebook.metadata["jupytext"] = notebook.metadata["jupytext"]
    else:
        piped_notebook.metadata.pop("jupytext", None)

    return piped_notebook

