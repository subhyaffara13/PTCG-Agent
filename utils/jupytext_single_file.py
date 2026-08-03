import copy
import json
import os
import re
import sys

def jupytext_single_file(nb_file, args, log, notary):
    """Apply the jupytext command, with given arguments, to a single file"""
    if nb_file == "-" and args.sync:
        msg = "Missing notebook path."
        if args.set_formats is not None and os.path.isfile(args.set_formats):
            msg += f" Did you mean 'jupytext --sync {args.set_formats}' ?"
        raise ValueError(msg)

    nb_dest = None
    if args.output:
        nb_dest = args.output
    elif nb_file == "-":
        nb_dest = "-"
    else:
        try:
            bp = base_path(nb_file, args.input_format)
        except InconsistentPath:
            if args.pre_commit_mode:
                log(
                    "[jupytext] Ignoring unmatched input path {}{}".format(
                        nb_file,
                        f" for format {args.input_format}" if args.input_format else "",
                    )
                )
                return 0
            raise
        if args.output_format:
            nb_dest = full_path(bp, args.output_format)

    config = load_jupytext_config(os.path.abspath(nb_file))

    def _read(path, fmt=None):
        """Read a notebook; mark cells trusted when the signature is valid."""
        nb = read(path, fmt=fmt, config=config)
        if notary.check_signature(nb):
            notary.mark_cells(nb, True)
        return nb

    def _writes(nb, fmt):
        """Serialize a notebook; sign the result when every cell is trusted."""
        content = writes(nb, fmt=fmt, config=config)
        if notary.check_cells(nb):
            notary.sign(reads(content, fmt=fmt, config=config))
        else:
            log("[jupytext] Warning: Notebook is not trusted")
        return content

    # Just acting on metadata / pipe => save in place
    save_in_place = not nb_dest and not args.sync
    if save_in_place:
        nb_dest = nb_file

    if nb_dest == "-":
        args.quiet = True

    # I. ### Read the notebook ###
    fmt = copy(args.input_format) or {}
    if not fmt:
        ext = os.path.splitext(nb_file)[1]
        if ext:
            fmt = {"extension": ext}
    if fmt:
        set_format_options(fmt, args.format_options)
    log(
        "[jupytext] Reading {}{}".format(
            nb_file if nb_file != "-" else "stdin",
            f" in format {short_form_one_format(fmt)}" if "extension" in fmt else "",
        )
    )

    timestamp_checker = TimestampChecker(pre_commit_mode=args.pre_commit_mode)
    timestamp_checker.get_and_check_timestamp(nb_file)
    notebook = _read(nb_file, fmt=fmt)

    if "extension" in fmt and "format_name" not in fmt:
        text_representation = notebook.metadata.get("jupytext", {}).get("text_representation", {})
        if text_representation.get("extension") == fmt["extension"]:
            fmt["format_name"] = text_representation["format_name"]

    # Compute actual extension when using script/auto, and update nb_dest if necessary
    dest_fmt = args.output_format
    if dest_fmt and dest_fmt["extension"] == ".auto":
        dest_fmt = check_auto_ext(dest_fmt, notebook.metadata, "--to")
        if not args.output and nb_file != "-":
            nb_dest = full_path(base_path(nb_file, args.input_format), dest_fmt)

    # Set the kernel
    set_kernel = args.set_kernel
    if (not set_kernel) and args.execute and notebook.metadata.get("kernelspec", {}).get("name") is None:
        set_kernel = "-"

    if set_kernel:
        if set_kernel == "-":
            language = (
                notebook.metadata.get("jupytext", {}).get("main_language") or notebook.metadata["kernelspec"]["language"]
            )

            if not language:
                raise ValueError("Cannot infer a kernel as notebook language is not defined")

            kernelspec = kernelspec_from_language(language)
        else:
            try:
                kernelspec = get_kernel_spec(set_kernel)
            except KeyError as err:
                raise KeyError(f"Please choose a kernel name among {find_kernel_specs().keys()}") from err

            kernelspec = {
                "name": args.set_kernel,
                "language": kernelspec.language,
                "display_name": kernelspec.display_name,
            }

        log("[jupytext] Setting kernel {}".format(kernelspec.get("name")))
        args.update_metadata["kernelspec"] = kernelspec

    # Read paired notebooks
    nb_files = [nb_file, nb_dest]
    outputs_nb_file = None
    if args.sync:
        # If we are also setting the formats, we take the information
        # from the --set-formats option
        if args.set_formats is not None:
            formats = long_form_multiple_formats(args.set_formats)
        else:
            formats = notebook_formats(notebook, config, nb_file, fallback_on_current_fmt=False)
        set_prefix_and_suffix(fmt, formats, nb_file)

        try:
            notebook, inputs_nb_file, outputs_nb_file = load_paired_notebook(
                notebook,
                fmt,
                config,
                formats,
                nb_file,
                log,
                args.pre_commit_mode,
                timestamp_checker,
                read_func=_read,
            )
            nb_files = [inputs_nb_file, outputs_nb_file]
        except NotAPairedNotebook as err:
            sys.stderr.write("[jupytext] Warning: " + str(err) + "\n")
            return 0
        except InconsistentVersions as err:
            sys.stderr.write("[jupytext] Error: " + str(err) + "\n")
            return 1

    # Are we updating a text file that has a metadata filter? #212
    if args.update_metadata or args.format_options:
        if notebook.metadata.get("jupytext", {}).get("notebook_metadata_filter") == "-all":
            notebook.metadata.get("jupytext", {}).pop("notebook_metadata_filter")

    # Update the metadata
    if args.update_metadata:
        log(f"[jupytext] Updating notebook metadata with '{json.dumps(args.update_metadata)}'")

        if "kernelspec" in args.update_metadata and "main_language" in notebook.metadata.get("jupytext", {}):
            notebook.metadata["jupytext"].pop("main_language")

        recursive_update(notebook.metadata, args.update_metadata)

    # II. ### Apply commands onto the notebook ###
    # Pipe the notebook into the desired commands
    if nb_file == "-":
        prefix = None
        directory = None
    else:
        prefix = os.path.splitext(os.path.basename(nb_file))[0]
        directory = os.path.dirname(nb_file)
    for cmd in args.pipe or []:
        notebook = pipe_notebook(
            notebook,
            cmd,
            args.pipe_fmt,
            quiet=args.quiet,
            prefix=prefix,
            directory=directory,
            warn_only=args.warn_only,
        )

    # and/or test the desired commands onto the notebook
    for cmd in args.check or []:
        pipe_notebook(
            notebook,
            cmd,
            args.pipe_fmt,
            update=False,
            quiet=args.quiet,
            prefix=prefix,
            directory=directory,
            warn_only=args.warn_only,
        )

    if (
        args.execute
        and args.pre_commit_mode
        and execution_counts_are_in_order(notebook)
        and not code_cells_have_changed(notebook, nb_files)
    ):
        log(f"[jupytext] Execution of {shlex.quote(nb_file)} skipped as code cells have not changed and outputs are present.")
        args.execute = False

    # Execute the notebook
    if args.execute:
        kernel_name = notebook.metadata.get("kernelspec", {}).get("name")
        log(f"[jupytext] Executing notebook with kernel {kernel_name}")

        if nb_dest is not None and nb_dest != "-":
            nb_path = os.path.dirname(nb_dest)
        elif nb_file != "-":
            nb_path = os.path.dirname(nb_file)
        else:
            nb_path = None

        run_path = args.run_path or nb_path
        if args.run_path and not os.path.isdir(run_path):
            # is this a relative directory?
            for base_dir in [nb_path, os.getcwd()]:
                try_path = os.path.join(base_dir, run_path)
                if os.path.isdir(try_path):
                    run_path = try_path
                    break
            if not os.path.isdir(run_path):
                raise ValueError(f"--run-path={args.run_path} is not a valid path")

        if run_path:
            resources = {"metadata": {"path": run_path}}
        else:
            resources = {}

        try:
            from nbconvert.preprocessors import ExecutePreprocessor

            exec_proc = ExecutePreprocessor(timeout=None, kernel_name=kernel_name)
            exec_proc.preprocess(notebook, resources=resources)
        except (ImportError, RuntimeError) as err:
            if args.pre_commit_mode:
                raise RuntimeError(
                    "An error occurred while executing the notebook. Please "
                    "make sure that you have listed 'nbconvert' and 'ipykernel' "
                    "under 'additional_dependencies' in the jupytext hook."
                ) from err
            raise RuntimeError(
                "An error occurred while executing the notebook. Please "
                "make sure that 'nbconvert' and 'ipykernel' are installed."
            ) from err

    # III. ### Possible actions ###
    # a. Test round trip conversion
    if args.test or args.test_strict:
        try:
            # Round trip from an ipynb document
            if fmt["extension"] == ".ipynb":
                test_round_trip_conversion(
                    notebook,
                    dest_fmt,
                    update=args.update,
                    allow_expected_differences=not args.test_strict,
                    stop_on_first_error=args.stop_on_first_error,
                )

            # Round trip from a text file
            else:
                # We read the original text from disk a second time
                with open(nb_file, encoding="utf-8") as fp:
                    org_text = fp.read()

                # We also make sure that the text file
                # has not changed since we first read it!
                timestamp_checker.check_timestamp(nb_file)

                # If the destination is not ipynb, we convert to/back that format
                if dest_fmt["extension"] != ".ipynb":
                    dest_text = writes(notebook, fmt=dest_fmt)
                    notebook = reads(dest_text, fmt=dest_fmt)

                text = writes(notebook, fmt=fmt, config=config)

                if args.test_strict:
                    compare(text, org_text)
                else:
                    # we ignore the YAML header in the comparison #414
                    comment = _SCRIPT_EXTENSIONS.get(fmt["extension"], {}).get("comment", "")
                    # white spaces between the comment char and the YAML delimiters are allowed
                    if comment:
                        comment = comment + r"\s*"
                    yaml_header = re.compile(
                        r"^{comment}---\s*\n.*\n{comment}---\s*\n".format(comment=comment),
                        re.MULTILINE | re.DOTALL,
                    )
                    compare(re.sub(yaml_header, "", text), re.sub(yaml_header, "", org_text))

        except (NotebookDifference, AssertionError) as err:
            sys.stdout.write(f"{nb_file}: {str(err)}")
            return 1
        return 0

    # b. Output to the desired file or format
    untracked_files = 0

    def lazy_write(
        path,
        fmt=None,
        action=None,
        update_timestamp_only=False,
        force_update_timestamp=False,
    ):
        """Write the notebook only if it has changed"""
        # Used in tests only
        if _callback_on_lazy_write is not None:
            _callback_on_lazy_write(path)
        if path == "-":
            timestamp_checker.check_all_timestamps()
            write(notebook, "-", fmt=fmt)
            return

        nonlocal untracked_files
        if update_timestamp_only:
            modified = False
        else:
            _, ext = os.path.splitext(path)
            fmt = copy(fmt or {})
            fmt = long_form_one_format(fmt, update={"extension": ext})
            new_content = _writes(notebook, fmt=fmt)
            diff = None
            if not new_content.endswith("\n"):
                new_content += "\n"
            if not os.path.isfile(path):
                modified = True
                diff = "(file did not exist)"
            else:
                # We load the current file from disk
                # NB: in the --to mode, it might be the first
                # time we actually read this file
                timestamp_checker.get_and_check_timestamp(path)
                with open(path, encoding="utf-8") as fp:
                    current_content = fp.read()

                timestamp_checker.check_timestamp(path)

                modified = new_content != current_content
                if modified and args.show_changes:
                    diff = compare(
                        new_content,
                        current_content,
                        "",
                        "",
                        return_diff=True,
                    )

        tmp_path = path
        if modified:
            # The text representation of the notebook has changed, we write it on disk
            create_prefix_dir(path, fmt, log)
            # Create a temporary file in the same directory as path. Later on we will move
            # that temporary file back to path (os.replace is atomic on most OS)
            name, ext = os.path.splitext(path)
            tmp_path = name + f"_tmp_jupytext_{os.getpid()}" + ext
            with open(tmp_path, "w", encoding="utf-8") as fp:
                fp.write(new_content)

        # We check that none of the input files changed while we were
        # doing our processing. If they did, we abort as we would
        # otherwise overwrite the modifications.
        try:
            timestamp_checker.check_all_timestamps()
        except SynchronousModificationError:
            if modified:
                os.remove(tmp_path)
            raise

        # When the content is unchanged, we still need to update the timestamp of
        # the text file to make sure they remain more recent than the ipynb file, for compatibility with the
        # Jupytext contents manager for Jupyter
        if args.use_source_timestamp:
            if tmp_path != nb_file:
                log(f"[jupytext] Setting the timestamp of {shlex.quote(path)} equal to that of {shlex.quote(nb_file)}")
                os.utime(tmp_path, (os.stat(nb_file).st_atime, os.stat(nb_file).st_mtime))
        elif not modified:
            if path.endswith(".ipynb"):
                # No need to update the timestamp of ipynb files
                log(f"[jupytext] Unchanged {shlex.quote(path)}")
            elif args.sync and not force_update_timestamp:
                # if the content is unchanged (and matches ipynb), we don't need
                # to update the timestamp as the contents manager will not throw in
                # that case (see the try/catch on read_pair(... must_match=True))
                log(f"[jupytext] Unchanged {shlex.quote(path)}")
            else:
                log(f"[jupytext] Updating the timestamp of {shlex.quote(path)}")
                os.utime(path, None)

        if modified:
            if action is None:
                message = f"[jupytext] Updating {shlex.quote(path)}"
            else:
                message = "[jupytext] Writing {path}{format}{action}".format(
                    path=shlex.quote(path),
                    format=(" in format " + short_form_one_format(fmt) if fmt and "format_name" in fmt else ""),
                    action=action,
                )
            if args.show_changes:
                message += " with this change:\n" + diff

            log(message)
            os.replace(tmp_path, path)

        # If we changed the file timestamp, we update our checker accordingly
        if modified or args.use_source_timestamp or force_update_timestamp:
            timestamp_checker.update_timestamp(path)

        if args.pre_commit:
            system("git", "add", path)

        if args.pre_commit_mode and is_untracked(path):
            log(
                f"[jupytext] Error: the git index is outdated.\n"
                f"Please add the paired notebook with:\n"
                f"    git add {shlex.quote(path)}"
            )
            untracked_files += 1

        return {"modified": modified}

    if nb_dest:
        if args.check_source_is_newer:
            ts_src = timestamp_checker.check_file_is_newest(nb_file)
            ts_dest = timestamp_checker.get_and_check_timestamp(nb_dest)
            if ts_dest is not None and ts_dest > ts_src:
                raise ValueError(f"Source {nb_file} is older than destination {nb_dest}")

        if nb_dest == nb_file and not dest_fmt:
            dest_fmt = fmt

        # Test consistency between dest name and output format
        if dest_fmt and nb_dest != "-":
            base_path(nb_dest, dest_fmt)

        # Describe what jupytext is doing
        if save_in_place:
            action = ""
        elif os.path.isfile(nb_dest) and args.update:
            if not nb_dest.endswith(".ipynb"):
                raise ValueError("--update is only for ipynb files")
            action = " (destination file updated)"
            check_file_version(notebook, nb_file, nb_dest)
            notebook = combine_inputs_with_outputs(notebook, read(nb_dest), fmt=fmt)
        elif os.path.isfile(nb_dest):
            suggest_update = " [use --update to preserve cell outputs and ids]" if nb_dest.endswith(".ipynb") else ""
            action = f" (destination file replaced{suggest_update})"
        else:
            action = ""

        formats = notebook.metadata.get("jupytext", {}).get("formats")
        formats = long_form_multiple_formats(formats)
        if formats:
            try:
                base_path_out, _ = find_base_path_and_format(nb_dest, formats)
            except InconsistentPath:
                # Drop 'formats' if the destination is not part of the paired notebooks
                formats = {}
                notebook.metadata.get("jupytext", {}).pop("formats")

        lazy_write(nb_dest, fmt=dest_fmt, action=action)

        nb_dest_in_pair = formats and any(
            os.path.exists(alt_path) and os.path.samefile(nb_dest, alt_path)
            for alt_path, _ in paired_paths(nb_file, fmt, formats)
        )

        if (
            nb_dest_in_pair
            and os.path.isfile(nb_file)
            and not nb_file.endswith(".ipynb")
            and os.path.isfile(nb_dest)
            and nb_dest.endswith(".ipynb")
        ):
            # If the destination is an ipynb file and is in the pair, then we
            # update the original text file timestamp, as required by our Content Manager
            # Otherwise Jupyter will refuse to open the paired notebook #335
            # NB: An alternative is --use-source-timestamp
            lazy_write(nb_file, update_timestamp_only=True)

    # c. Synchronize paired notebooks
    elif args.sync:
        if args.check_source_is_newer:
            timestamp_checker.check_file_is_newest(nb_file)
        write_pair(nb_file, formats, lazy_write)

    return untracked_files

