
def module_not_found(
    manager: BuildManager,
    line: int,
    caller_state: State,
    target: str,
    reason: ModuleNotFoundReason,
) -> None:
    errors = manager.errors
    save_import_context = errors.import_context()
    errors.set_import_context(caller_state.import_context)
    errors.set_file(caller_state.xpath, caller_state.id, caller_state.options)
    errors.set_file_ignored_lines(
        caller_state.xpath,
        caller_state.tree.ignored_lines if caller_state.tree else caller_state.imports_ignored,
        caller_state.ignore_all or caller_state.options.ignore_errors,
    )
    if target == "builtins":
        manager.error(
            line, 'Cannot find "builtins" module. Typeshed appears broken!', blocker=True
        )
        errors.raise_error()
    else:
        daemon = manager.options.fine_grained_incremental
        msg, notes = reason.error_message_templates(daemon)
        if reason == ModuleNotFoundReason.NOT_FOUND:
            code = codes.IMPORT_NOT_FOUND
        elif (
            reason == ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS
            or reason == ModuleNotFoundReason.APPROVED_STUBS_NOT_INSTALLED
        ):
            code = codes.IMPORT_UNTYPED
        else:
            code = codes.IMPORT
        manager.error(line, msg.format(module=target), code=code)

        if (
            reason == ModuleNotFoundReason.NOT_FOUND
            and not errors.prefer_simple_messages()
            and errors.is_error_code_enabled(code)
            and line not in errors.ignored_lines.get(caller_state.xpath, {})
        ):
            top_level_target = target.split(".")[0]
            if not top_level_target.startswith("_"):
                known_modules = get_known_modules(
                    manager.find_module_cache.stdlib_py_versions, manager.options.python_version
                )
                matches = best_matches(top_level_target, known_modules, n=3)
                matches = [m for m in matches if m.lower() != top_level_target.lower()]
                if matches:
                    errors.report(
                        line,
                        0,
                        f'Did you mean {pretty_seq(matches, "or")}?',
                        severity="note",
                        code=code,
                    )

        dist = stub_distribution_name(target)
        for note in notes:
            if "{stub_dist}" in note:
                assert dist is not None
                note = note.format(stub_dist=dist)
            manager.note(line, note, only_once=True, code=code)
        if reason is ModuleNotFoundReason.APPROVED_STUBS_NOT_INSTALLED:
            assert dist is not None
            manager.missing_stub_packages.add(dist)
    errors.set_import_context(save_import_context)

