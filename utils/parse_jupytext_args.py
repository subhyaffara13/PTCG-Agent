import json

def parse_jupytext_args(args=None):
    """Command line parser for jupytext"""

    parser = argparse.ArgumentParser(
        description="Jupyter Notebooks as Markdown Documents, Julia, Python or R Scripts",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Input
    parser.add_argument(
        "notebooks",
        help="One or more notebook(s). Notebook is read from stdin when this argument is empty.",
        nargs="*",
    )
    parser.add_argument(
        "--from",
        dest="input_format",
        help="Jupytext format for the input(s). Inferred from the file extension and content when missing.",
    )
    # Destination format & act on metadata

    selected_file_extensions = ["md", "Rmd", "jl", "py", "R"]
    parser.add_argument(
        "--to",
        dest="output_format",
        help=(
            "The destination format: 'ipynb', 'markdown' or 'script', or a file extension: "
            "'{}', ... or 'auto' (script extension matching the notebook language), "
            "or a combination of an extension and a format name, e.g. {} ".format(
                "', '".join(selected_file_extensions),
                ", ".join({f"md:{fmt.format_name}" for fmt in JUPYTEXT_FORMATS if fmt.extension == ".md"}),
            )
            + " or {}. ".format(", ".join({f"py:{fmt.format_name}" for fmt in JUPYTEXT_FORMATS if fmt.extension == ".py"}))
            + "The default format for scripts is the 'percent' format, "
            "which uses '# %%%%' as cell markers and is compatible with VS Code and PyCharm. "
            "Alternatively, you can also use the 'light' format, which uses fewer cell markers. "
            "The main formats (MyST Markdown, Markdown, percent, light) preserve "
            "notebooks and text documents in a roundtrip. Use the "
            "--test and and --test-strict commands to test the roundtrip on your files. "
            "Read more about the available formats at "
            "https://jupytext.org/formats/scripts/ "
            "NB: in addition to the extensions listed above, you can also use these: '{}'".format(
                "', '".join(
                    sorted(
                        {ext.removeprefix(".") for ext in NOTEBOOK_EXTENSIONS}
                        - set(selected_file_extensions + ["auto", "ipynb"])
                    )
                )
            )
        ),
    )

    # Destination file
    parser.add_argument(
        "-o",
        "--output",
        help="Destination file. Defaults to the original file, "
        "with prefix/suffix/extension changed according to "
        "the destination format. "
        "Use '-' to print the notebook on stdout.",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Preserve the output cells when the destination notebook is an .ipynb file that already exists",
    )

    parser.add_argument(
        "--set-formats",
        type=str,
        help="Turn the notebook or text document to one or more alternative representations "
        "with e.g. '--set-formats ipynb,py:light'. "
        "The --set-formats option also triggers the creation/update of all paired files",
    )

    # Action: convert(default)/version/list paired paths/sync/apply/test
    action = parser.add_mutually_exclusive_group()
    action.add_argument(
        "--sync",
        "-s",
        help="Synchronize the content of the paired representations of "
        "the given notebook. Input cells are taken from the file that "
        "was last modified, and outputs are read from the ipynb file, "
        "if present.",
        action="store_true",
    )
    action.add_argument(
        "--paired-paths",
        "-p",
        help="List the locations of the alternative representations for this notebook.",
        action="store_true",
    )
    parser.add_argument(
        "--format-options",
        "--opt",
        action="append",
        help="Set format options with e.g. '--opt comment_magics=true' or '--opt notebook_metadata_filter=-kernelspec'.",
    )
    parser.add_argument(
        "--update-metadata",
        default={},
        type=json.loads,
        help="Update the notebook metadata with the desired dictionary. "
        "Argument must be given in JSON format. For instance, if you "
        "want to activate a pairing in the generated file, use e.g. "
        """--update-metadata '{"jupytext":{"formats":"ipynb,py:light"}}' """
        "See also the --opt and --set-formats options for other ways "
        "to operate on the Jupytext metadata.",
    )
    parser.add_argument(
        "--use-source-timestamp",
        help="Set the modification timestamp of the output file(s) equal"
        "to that of the source file, and keep the source file and "
        "its timestamp unchanged.",
        action="store_true",
    )
    parser.add_argument(
        "--check-source-is-newer",
        help="Check that the file given as argument is the most recent of all paired files, and "
        "if applicable, checks that it is newer than the destination file.",
        action="store_true",
    )
    parser.add_argument(
        "--warn-only",
        "-w",
        action="store_true",
        help="Only issue a warning and continue processing other notebooks when the conversion of a given notebook fails",
    )
    action.add_argument(
        "--test",
        action="store_true",
        help="Test that the notebook is stable under a round trip conversion, up to the expected changes",
    )
    action.add_argument(
        "--test-strict",
        action="store_true",
        help="Test that the notebook is strictly stable under a round trip conversion",
    )
    parser.add_argument(
        "--stop",
        "-x",
        dest="stop_on_first_error",
        action="store_true",
        help="In --test mode, stop on first round trip conversion error, and report stack traceback",
    )

    # Pipe notebook inputs into other commands
    parser.add_argument(
        "--pipe",
        action="append",
        help="Pipe the text representation (in format --pipe-fmt) of the notebook into "
        "another program, and read the notebook back. For instance, reformat "
        "your notebook with: "
        "'jupytext notebook.ipynb --pipe black' "
        "If you want to reformat it and sync the paired representation, execute: "
        "'jupytext notebook.ipynb --sync --pipe black' "
        "In case the program that you want to execute does not accept pipes, use {} "
        "as a placeholder for a temporary file name into which jupytext will "
        "write the text representation of the notebook, e.g.: "
        "jupytext notebook.ipynb --pipe 'black {}'",
    )
    parser.add_argument(
        "--diff",
        "-d",
        action="store_true",
        help="Show the differences between (the inputs) of two notebooks",
    )
    parser.add_argument(
        "--diff-format",
        help="The text format used to show differences in --diff",
    )
    parser.add_argument(
        "--check",
        action="append",
        help="Pipe the text representation (in format --pipe-fmt) of the notebook into "
        "another program, and test that the returned value is non zero. For "
        "instance, test that your notebook is pep8 compliant with: "
        "'jupytext notebook.ipynb --check flake8' "
        "or run pytest on your notebook with: "
        "'jupytext notebook.ipynb --check pytest' "
        "In case the program that you want to execute does not accept pipes, use {} "
        "as a placeholder for a temporary file name into which jupytext will "
        "write the text representation of the notebook, e.g.: "
        "jupytext notebook.ipynb --check 'pytest {}'",
    )
    parser.add_argument(
        "--pipe-fmt",
        default="auto:percent",
        help="The format in which the notebook should be piped to other programs, "
        "when using the --pipe and/or --check commands.",
    )

    # Execute the notebook
    parser.add_argument(
        "--set-kernel",
        "-k",
        type=str,
        help="Set the kernel with the given name on the notebook. "
        "Use '--set-kernel -' to set a kernel matching the current "
        "environment on Python notebooks, and matching the notebook "
        "language otherwise (get the list of available kernels with "
        "'jupyter kernelspec list')",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute the notebook with the given kernel. In the "
        "--pre-commit-mode, the notebook is executed only if a code "
        "cell changed, or if some execution outputs are missing "
        "or not ordered.",
    )
    parser.add_argument(
        "--run-path",
        type=str,
        help="Execute the notebook at the given path (defaults to the notebook parent directory)",
    )

    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Quiet mode: do not comment about files being updated or created",
    )
    parser.add_argument(
        "--show-changes",
        action="store_true",
        help="Display the diff for each output file",
    )

    action.add_argument(
        "--version",
        "-v",
        action="store_true",
        help="Show jupytext's version number and exit",
    )

    parser.add_argument(
        "--pre-commit",
        action="store_true",
        help="Ignore the notebook argument, and instead apply Jupytext "
        "on the notebooks found in the git index, which have an "
        "extension that matches the (optional) --from argument.",
    )
    parser.add_argument(
        "--pre-commit-mode",
        action="store_true",
        help="This is a mode that is compatible with the pre-commit framework. "
        "In this mode, --sync won't use timestamp but instead will "
        "determines the source notebook as the element of the pair "
        "that is added to the git index. An alert is raised if multiple inconsistent representations are "
        "in the index. It also raises an alert after updating the paired files or outputs if those "
        "files need to be added to the index. Finally, filepaths that aren't in the source format "
        "you are trying to convert from are ignored.",
    )

    return parser.parse_args(args)

