
def jupytext(args=None, *, notary=None):
    """Entry point for the jupytext script"""
    args = parse_jupytext_args(args)

    def log(text):
        if not args.quiet:
            sys.stdout.write(text + "\n")

    if args.version:
        log(__version__)
        return 0

    if args.pre_commit:
        warnings.warn(
            "The --pre-commit argument is deprecated. "
            "Please consider switching to the pre-commit.com framework "
            "(let us know at https://github.com/jupytext/jupytext/issues "
            "if that is an issue for you)",
            DeprecationWarning,
        )
        if args.notebooks:
            raise ValueError("--pre-commit takes notebooks from the git index. Do not pass any notebook here.")
        args.notebooks = notebooks_in_git_index(args.input_format)
        log("[jupytext] Notebooks in git index are:")
        for nb_file in args.notebooks:
            log(nb_file)

    # Read notebook from stdin
    if not args.notebooks:
        if not args.pre_commit:
            args.notebooks = ["-"]

    if args.set_formats is not None:
        # Replace empty string with None
        args.update_metadata = recursive_update(args.update_metadata, {"jupytext": {"formats": args.set_formats or None}})
        args.sync = True

    if args.paired_paths:
        if len(args.notebooks) != 1:
            raise ValueError("--paired-paths applies to a single notebook")
        print_paired_paths(args.notebooks[0], args.input_format)
        return 1

    if args.run_path:
        args.execute = True

    if (args.test or args.test_strict) and not args.output_format and not args.output and not args.sync:
        raise ValueError("Please provide one of --to, --output or --sync")

    if (
        not args.output_format
        and not args.output
        and not args.sync
        and not args.pipe
        and not args.diff
        and not args.check
        and not args.update_metadata
        and not args.format_options
        and not args.set_kernel
        and not args.execute
    ):
        raise ValueError(
            "Please provide one of --to, --output, --set-formats, --sync, --pipe, --diff, "
            "--check, --update-metadata, --format-options, --set-kernel or --execute"
        )

    if args.diff:
        if (
            len(args.notebooks) != 2
            or args.output_format
            or args.output
            or args.sync
            or args.pipe
            or args.check
            or args.update_metadata
            or args.format_options
            or args.set_kernel
            or args.execute
        ):
            raise ValueError(
                "Please provide two notebooks after 'jupytext --diff'.\n"
                "NB: Use --show-changes if you wish to see the changes in "
                "a notebook being updated by Jupytext."
            )

        nb_file1, nb_file2 = args.notebooks
        nb1 = read(nb_file1)
        nb2 = read(nb_file2)

        def fmt_if_not_ipynb(nb):
            fmt = nb.metadata["jupytext"]["text_representation"]
            if fmt["extension"] == ".ipynb":
                return None
            return short_form_one_format(fmt)

        diff_fmt = args.diff_format or fmt_if_not_ipynb(nb1) or fmt_if_not_ipynb(nb2) or "md"

        diff = compare(
            writes(nb2, diff_fmt),
            writes(nb1, diff_fmt),
            nb_file2,
            nb_file1,
            return_diff=True,
        )
        sys.stdout.write(diff)

        return

    if args.output and len(args.notebooks) != 1:
        raise ValueError("Please input a single notebook when using --output")

    # Warn if '--to' is used in place of '--output'
    if (
        not args.output
        and args.output_format
        and "." in args.output_format
        # a suffix is expected to start with one of these characters #901
        and not args.output_format.startswith((".", "-", "_"))
        and "//" not in args.output_format
    ):

        def single_line(msg, *args, **kwargs):
            return f"[warning] {msg}\n"

        warnings.formatwarning = single_line
        warnings.warn(
            "You might have passed a file name to the '--to' option, "
            "when a format description was expected. Maybe you want to use the '-o' option instead?"
        )

    if args.input_format:
        args.input_format = long_form_one_format(args.input_format)

    if args.output_format:
        args.output_format = long_form_one_format(args.output_format)
        set_format_options(args.output_format, args.format_options)

    # Wildcard extension on Windows #202
    notebooks = []
    for pattern in args.notebooks:
        if "*" in pattern or "?" in pattern:
            # Exclude the .jupytext.py configuration file
            notebooks.extend(glob.glob(pattern, recursive=True))
        else:
            notebooks.append(pattern)

    # Count how many files have round-trip issues when testing
    exit_code = 0

    notary_to_close = None
    if notary is None:
        notary = notary_to_close = NotebookNotary()

    try:
        for nb_file in notebooks:
            if not args.warn_only:
                exit_code += jupytext_single_file(nb_file, args, log, notary=notary)
            else:
                try:
                    exit_code += jupytext_single_file(nb_file, args, log, notary=notary)
                except Exception as err:
                    sys.stderr.write(f"[jupytext] Error: {str(err)}\n")

        return exit_code
    finally:
        if notary_to_close:
            notary_to_close.store.close()

